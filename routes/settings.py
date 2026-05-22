"""
routes/settings.py — API para la gestión dinámica de configuraciones SaaS.
Usa SQLAlchemy ORM (Pilar 3) para todas las operaciones de escritura.
"""
import logging
from typing import Annotated, Optional, List, Any

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from core.auth import require_admin
from core.database import get_session_dep
from core.models import StatusMapping, CostCenterMapping, AppSetting, Holiday, ConfigQuery
from core.db_config_manager import load_config_to_memory, get_setting, get_status_mapping, get_cost_center_mapping, get_holidays
from core.app_instance import templates
from core.utils import sanitize_for_json
from core.state import AppState, get_app_state

logger = logging.getLogger("routes-settings")
router = APIRouter(dependencies=[Depends(require_admin)])

# Tipo de dependencia reutilizable
DBSession = Annotated[Session, Depends(get_session_dep)]

def invalidate_caches(db: Session):
    """Limpia el caché global en memoria y elimina todos los snapshots de base de datos."""
    from core.state import AppState, get_app_state
    from sqlalchemy import text
    try:
        state.clear_cache()
        logger.info("Caché en memoria invalidado por actualización de configuración.")
    except Exception as e:
        logger.warning(f"Error al limpiar caché en memoria: {e}")
        
    try:
        db.execute(text("DELETE FROM analytics_snapshots"))
        db.flush()
        logger.info("Snapshots de base de datos eliminados por actualización de configuración.")
    except Exception as e:
        logger.warning(f"Error al limpiar la tabla de snapshots (puede no existir aún): {e}")

# ─── Pydantic Models ──────────────────────────────────────────────────────────
class SettingUpdate(BaseModel):
    key: str
    value: str

class StatusMappingUpdate(BaseModel):
    code: str
    label: str

class CostCenterMappingUpdate(BaseModel):
    center_code: str
    business_area: str

class HolidayAdd(BaseModel):
    date_str: str  # ISO format: YYYY-MM-DD

class QueryUpdate(BaseModel):
    query_id: str
    # DEPRECADO: solo se mantiene para compatibilidad con api_query_preview heredado.
    # Los nuevos consumidores deben enviar únicamente visual_state.
    sql_text: Optional[str] = None
    params: Optional[List[Any]] = None
    visual_state: Optional[str] = None

class JoinDef(BaseModel):
    table: str
    onLeft: str
    onRight: str

class FilterDef(BaseModel):
    column: str
    operator: str
    value: Optional[str] = ""
    valueType: Optional[str] = "value"  # "value", "column", or "date_diff"
    compareColumn: Optional[str] = None
    offsetValue: Optional[str] = None

class MetricDef(BaseModel):
    column: str
    aggregation: str
    format: Optional[str] = "number"

class TimeAxisDef(BaseModel):
    column: str
    granularity: str

class SecondMetricDef(BaseModel):
    column: str = ""
    aggregation: str = ""
    label: str = ""

class VisualQueryBuilderPayload(BaseModel):
    baseTable: str
    joins: list[JoinDef] = []
    filters: list[FilterDef] = []
    metric: MetricDef
    timeAxis: TimeAxisDef
    breakdown: str | None = None
    secondMetric: Optional[SecondMetricDef] = None


# ─── Vista (UI) ───────────────────────────────────────────────────────────────
@router.get("/settings", response_class=HTMLResponse)
async def settings_view(request: Request, db: DBSession, state: AppState = Depends(get_app_state)):
    """Renderiza el panel de control de configuraciones SaaS."""
    context = {
        "request": request,
        "status_mapping": get_status_mapping(),
        "cost_centers": get_cost_center_mapping(),
        "holidays": get_holidays(),
        "settings": {
            "HEADER_DENSITY_THRESHOLD": get_setting("HEADER_DENSITY_THRESHOLD"),
            "HEADER_MIN_COLS": get_setting("HEADER_MIN_COLS"),
            "HEADER_SCAN_LIMIT": get_setting("HEADER_SCAN_LIMIT"),
            "DEFAULT_ENCODING": get_setting("DEFAULT_ENCODING"),
            "DEFAULT_SEPARATOR": get_setting("DEFAULT_SEPARATOR"),
            "MAX_COLUMN_BUFFER": get_setting("MAX_COLUMN_BUFFER"),
        }
    }
    response = templates.TemplateResponse(request=request, name="settings.html", context=context)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response


# ─── API: Settings Generales ─────────────────────────────────────────────────
@router.get("/api/settings")
def api_get_settings(state: AppState = Depends(get_app_state)):
    return {
        "status_mapping": get_status_mapping(),
        "cost_centers": get_cost_center_mapping(),
        "app_settings": {
            k: get_setting(k) for k in [
                "HEADER_DENSITY_THRESHOLD", "HEADER_MIN_COLS", "HEADER_SCAN_LIMIT",
                "DEFAULT_ENCODING", "DEFAULT_SEPARATOR", "MAX_COLUMN_BUFFER"
            ]
        }
    }

@router.post("/api/settings/update")
def api_update_setting(update: SettingUpdate, db: DBSession, state: AppState = Depends(get_app_state)):
    row = db.query(AppSetting).filter(AppSetting.key == update.key).first()
    if not row:
        raise HTTPException(status_code=404, detail="Configuración no encontrada")
    row.value = update.value
    db.flush()
    load_config_to_memory(db)
    invalidate_caches(db)
    return {"status": "success", "message": "Configuración actualizada"}


@router.post("/api/settings/status")
def api_upsert_status(update: StatusMappingUpdate, db: DBSession, state: AppState = Depends(get_app_state)):
    row = db.query(StatusMapping).filter(StatusMapping.code == update.code).first()
    if row:
        row.label = update.label
    else:
        db.add(StatusMapping(code=update.code, label=update.label))
    db.flush()
    load_config_to_memory(db)
    invalidate_caches(db)
    return {"status": "success", "message": "Estado actualizado"}

@router.delete("/api/settings/status/{code}")
def api_delete_status(code: str, db: DBSession, state: AppState = Depends(get_app_state)):
    row = db.query(StatusMapping).filter(StatusMapping.code == code).first()
    if not row:
        raise HTTPException(status_code=404, detail="Código no encontrado")
    db.delete(row)
    db.flush()
    load_config_to_memory(db)
    invalidate_caches(db)
    return {"status": "success"}


@router.post("/api/settings/cost_center")
def api_upsert_cost_center(update: CostCenterMappingUpdate, db: DBSession, state: AppState = Depends(get_app_state)):
    row = db.query(CostCenterMapping).filter(CostCenterMapping.center_code == update.center_code).first()
    if row:
        row.business_area = update.business_area
    else:
        db.add(CostCenterMapping(center_code=update.center_code, business_area=update.business_area))
    db.flush()
    load_config_to_memory(db)
    invalidate_caches(db)
    return {"status": "success", "message": "Centro de costo actualizado"}

@router.delete("/api/settings/cost_center/{code}")
def api_delete_cost_center(code: str, db: DBSession, state: AppState = Depends(get_app_state)):
    row = db.query(CostCenterMapping).filter(CostCenterMapping.center_code == code).first()
    if not row:
        raise HTTPException(status_code=404, detail="Centro de costo no encontrado")
    db.delete(row)
    db.flush()
    load_config_to_memory(db)
    invalidate_caches(db)
    return {"status": "success"}


# ─── API: Feriados ────────────────────────────────────────────────────────────
@router.post("/api/settings/holiday")
def api_add_holiday(h: HolidayAdd, db: DBSession, state: AppState = Depends(get_app_state)):
    existing = db.query(Holiday).filter(Holiday.date_str == h.date_str).first()
    if existing:
        return {"status": "exists", "message": "El feriado ya existe"}
    db.add(Holiday(date_str=h.date_str))
    db.flush()
    load_config_to_memory(db)
    invalidate_caches(db)
    return {"status": "success", "message": f"Feriado {h.date_str} añadido"}

@router.post("/api/settings/holidays/sync")
def api_sync_holidays(db: DBSession, state: AppState = Depends(get_app_state)):
    """Sincroniza automáticamente los feriados nacionales (Chile) usando la librería holidays."""
    import holidays
    from datetime import datetime
    try:
        # Años actual y siguiente
        years = [datetime.now().year, datetime.now().year + 1]
        cl_holidays = holidays.Chile(years=years)
        
        added_count = 0
        for date_obj, name in cl_holidays.items():
            # El objeto date de la librería holidays es compatible con strftime
            d_str = date_obj.strftime("%Y-%m-%d")
            existing = db.query(Holiday).filter(Holiday.date_str == d_str).first()
            if not existing:
                db.add(Holiday(date_str=d_str))
                added_count += 1
        
        db.flush()
        load_config_to_memory(db)
        invalidate_caches(db)
        return {"status": "success", "message": f"Sincronización exitosa. Se detectaron {added_count} nuevos feriados chilenos para {years}."}
    except Exception as e:
        logger.error(f"Error sincronizando feriados: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en la sincronización: {str(e)}")

@router.delete("/api/settings/holiday/{date_str}")
def api_delete_holiday(date_str: str, db: DBSession, state: AppState = Depends(get_app_state)):
    row = db.query(Holiday).filter(Holiday.date_str == date_str).first()
    if not row:
        raise HTTPException(status_code=404, detail="Feriado no encontrado")
    db.delete(row)
    db.flush()
    load_config_to_memory(db)
    invalidate_caches(db)
    return {"status": "success"}


# ─── API: Consultas SQL ───────────────────────────────────────────────────────
@router.get("/api/queries/{query_id}")
def api_get_query(query_id: str, db: DBSession, state: AppState = Depends(get_app_state)):
    """
    Retorna el estado visual (JSON) de una consulta del Analytics Studio.
    No expone sql_text al cliente: el SQL se compila en tiempo de ejecución
    mediante api_build_sql a partir del visual_state.
    """
    row = db.query(ConfigQuery).filter(ConfigQuery.query_id == query_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Consulta no encontrada")
    return {
        "query_id":        row.query_id,
        "visual_state":    row.visual_state,
        "has_visual_state": bool(row.visual_state),
        # sql_text solo se expone cuando no hay visual_state (queries de solo SQL sin constructor visual)
        "sql_text":        row.sql_text if not row.visual_state else None,
    }

@router.post("/api/settings/query")
def api_update_query(update: QueryUpdate, db: DBSession, state: AppState = Depends(get_app_state)):
    """
    Persiste el estado visual (JSON) de una consulta. Solo acepta visual_state;
    nunca escribe sql_text desde la UI: el SQL es siempre derivado en tiempo
    de ejecución por api_build_sql a partir del visual_state almacenado.
    """
    if not update.visual_state:
        raise HTTPException(
            status_code=422,
            detail="Se requiere 'visual_state'. El SQL crudo no es aceptado por este endpoint."
        )
    row = db.query(ConfigQuery).filter(ConfigQuery.query_id == update.query_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Consulta no encontrada")
    row.visual_state = update.visual_state
    # sql_text NO se actualiza: permanece como fallback de compatibilidad
    # y será limpiado progresivamente en la Fase 2.
    db.flush()
    load_config_to_memory(db)
    invalidate_caches(db)
    return {"status": "success", "message": "Estado visual actualizado correctamente"}

# ─── API: Estudio de Analíticas (Introspección y Preview) ───────────────────
@router.get("/api/studio/schema")
def api_get_schema(db: DBSession, state: AppState = Depends(get_app_state)):
    """Retorna el listado de tablas y sus columnas para el editor."""
    from sqlalchemy import text
    tables = {}
    ALLOWED_TABLES = {'outbound_deliveries', 'stock_levels', 'warehouse_tasks', 'inventory_movements'}
    try:
        # SQLite: Obtener tablas permitidas
        res_tables = db.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")).all()
        for t in res_tables:
            t_name = t[0]
            if t_name not in ALLOWED_TABLES:
                continue
                
            cols = db.execute(text(f"PRAGMA table_info({t_name})")).all()
            tables[t_name] = [c[1] for c in cols] # c[1] es el nombre de la columna
        return tables
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/studio/preview")
async def api_query_preview(update: QueryUpdate, db: DBSession, state: AppState = Depends(get_app_state)):
    """Ejecuta una consulta temporal y retorna datos para previsualización."""
    import pandas as pd
    from sqlalchemy import text
    from repositories.deliveries import DeliveriesRepository
    AREA_EXPR = DeliveriesRepository.AREA_EXPR
    
    sql = update.sql_text

    # Guard: rechazar SQL vacío/None o el string literal "undefined" que JS envía
    # cuando document.getElementById('editQueryText') no existe en el DOM.
    if not sql or not sql.strip() or sql.strip().lower() == "undefined":
        return {"error": "El campo SQL está vacío. Escribe o selecciona una consulta antes de previsualizar."}

    if "{AREA_EXPR}" in sql:
        sql = sql.replace("{AREA_EXPR}", AREA_EXPR)
        
    try:
        # 1. Identificar parámetros necesarios para el preview
        import re
        param_count = sql.count("?")
        params_dict = {}
        sql_preview = sql
        
        # Convertimos '?' a ':p0', ':p1', etc. para compatibilidad con SQLAlchemy text()
        for i in range(param_count):
            placeholder = f"p{i}"
            # Reemplazar solo la primera ocurrencia de '?' en cada iteración
            sql_preview = sql_preview.replace("?", f":{placeholder}", 1)
            
            # Si el frontend nos provee los parámetros del constructor visual, usarlos exactamente!
            if update.params is not None and i < len(update.params):
                params_dict[placeholder] = update.params[i]
            else:
                # Lógica heurística heredada para fallback
                if "retraso" in sql.lower() and i == 0:
                    params_dict[placeholder] = 2
                else:
                    params_dict[placeholder] = "2026%"
        
        # 2. Ejecutar con límite de seguridad
        # db.bind está deprecado en SQLAlchemy 2.x → usar db.connection()
        df = pd.read_sql(text(sql_preview), db.connection(), params=params_dict)
        df = df.head(100)
        
        # 3. Saneamiento ULTRA-SEGURO
        records = df.to_dict(orient="records")
        sanitized = sanitize_for_json(records)
        
        logger.info(f"Studio Preview exitoso para SQL: {sql[:50]}... (Filas: {len(sanitized)})")
        return sanitized
    except Exception as e:
        logger.error(f"Error en Studio Preview ({sql[:50]}...): {str(e)}")
        return {"error": str(e)}

# ─── API: Visual Query Builder ───────────────────────────────────────────────
# validate_identifier y ALLOWED_TABLES viven ahora en core/query_engine.
# Este endpoint es una capa de transporte HTTP delgada que delega al motor.
from core.query_engine import build_sql_from_payload

@router.post("/api/studio/build_sql")
def api_build_sql(payload: VisualQueryBuilderPayload, db: DBSession, state: AppState = Depends(get_app_state)):
    """
    Compila el estado visual del constructor en SQL parametrizado seguro.
    La validación de identifiers y la construcción SQL están en core/query_engine.
    """
    sql, bound_params = build_sql_from_payload(payload, db)
    return {
        "status": "success",
        "sql_text": sql,
        "bound_params": bound_params,
    }
