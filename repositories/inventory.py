import logging
import pandas as pd
from sqlalchemy import text
from datetime import datetime
from .base import BaseRepository

logger = logging.getLogger("repo-inventory")

class InventoryRepository(BaseRepository):
    """Repositorio para el dominio de Movimientos de Inventario y Consumos."""

    def get_consumos_ceco(self, ceco: str) -> dict:
        ceco_clean = ceco.strip().upper()
        try:
            # Consulta Histórica (con dedup)
            query_hist = f"""
                SELECT
                    material,
                    MAX(texto_breve_material) as descripcion,
                    MAX(umb) as umb,
                    SUM(cantidad) * -1 as cantidad_total,
                    SUM(importe_ml) * -1 as costo_total,
                    (
                        SELECT ABS(importe_ml / cantidad)
                        FROM inventory_movements i2
                        WHERE UPPER(TRIM(i2.material)) = UPPER(TRIM(inventory_movements.material))
                          AND i2.cantidad != 0
                          AND i2.cmv = '201'
                        ORDER BY substr(i2.fe_contab, 7, 4) || '-' || substr(i2.fe_contab, 4, 2) || '-' || substr(i2.fe_contab, 1, 2) DESC, i2.hora DESC
                        LIMIT 1
                    ) as precio_unitario
                FROM inventory_movements
                WHERE cmv = '201'
                  AND UPPER(TRIM(ce_coste)) = :ceco
                  AND fe_contab LIKE :year
                GROUP BY material
                ORDER BY costo_total DESC
            """
            current_year_str = str(datetime.now().year)
            df_hist = pd.read_sql(text(query_hist), self.session.connection(), params={"ceco": ceco_clean, "year": f"%{current_year_str}"})
            df_hist = df_hist.astype(object).where(pd.notnull(df_hist), None)
    
            # Consulta Mes Actual (con dedup)
            current_month_str = datetime.now().strftime('%m-%Y')
            query_mes = f"""
                SELECT
                    material,
                    MAX(texto_breve_material) as descripcion,
                    MAX(umb) as umb,
                    SUM(cantidad) * -1 as cantidad_total,
                    SUM(importe_ml) * -1 as costo_total,
                    (
                        SELECT ABS(importe_ml / cantidad)
                        FROM inventory_movements i2
                        WHERE UPPER(TRIM(i2.material)) = UPPER(TRIM(inventory_movements.material))
                          AND i2.cantidad != 0
                          AND i2.cmv = '201'
                        ORDER BY substr(i2.fe_contab, 7, 4) || '-' || substr(i2.fe_contab, 4, 2) || '-' || substr(i2.fe_contab, 1, 2) DESC, i2.hora DESC
                        LIMIT 1
                    ) as precio_unitario
                FROM inventory_movements
                WHERE cmv = '201'
                  AND UPPER(TRIM(ce_coste)) = :ceco
                  AND fe_contab LIKE :month
                GROUP BY material
                ORDER BY costo_total DESC
            """
            df_mes = pd.read_sql(text(query_mes), self.session.connection(), params={"ceco": ceco_clean, "month": f"%{current_month_str}"})
            df_mes = df_mes.astype(object).where(pd.notnull(df_mes), None)
    
            return {
                "historico": df_hist.to_dict(orient="records"),
                "mes_actual": df_mes.to_dict(orient="records")
            }
        except Exception as e:
            logger.error(f"Error fetching consumos for CeCo {ceco}: {e}")
            raise

    def get_consumos_materiales(self, materiales: list) -> dict:
        mats_clean = [m.strip().upper() for m in materiales if m.strip()]
        if not mats_clean:
            return {"data": []}
    
        try:
            placeholders = ",".join([f":m{i}" for i in range(len(mats_clean))])
            params = {f"m{i}": m for i, m in enumerate(mats_clean)}
    
            current_month_str = datetime.now().strftime('%m-%Y')
            current_year_str = str(datetime.now().year)
    
            query = f"""
                SELECT
                    material,
                    MAX(texto_breve_material) as descripcion,
                    MAX(umb) as umb,
                    COALESCE((SELECT MAX(area_negocio)
                     FROM outbound_deliveries o
                     WHERE UPPER(TRIM(o.centro_costo)) = UPPER(TRIM(inventory_movements.ce_coste))
                       AND o.area_negocio IS NOT NULL
                       AND TRIM(o.area_negocio) != ''), 'SIN AREA') as area_negocio,
                    SUM(CASE WHEN fe_contab LIKE :month THEN cantidad ELSE 0 END) * -1 as cantidad_mes,
                    SUM(CASE WHEN fe_contab LIKE :month THEN importe_ml ELSE 0 END) * -1 as costo_mes,
                    SUM(cantidad) * -1 as cantidad_total,
                    SUM(importe_ml) * -1 as costo_total,
                    (
                        SELECT ABS(importe_ml / cantidad)
                        FROM inventory_movements i2
                        WHERE UPPER(TRIM(i2.material)) = UPPER(TRIM(inventory_movements.material))
                          AND i2.cantidad != 0
                          AND i2.cmv = '201'
                        ORDER BY substr(i2.fe_contab, 7, 4) || '-' || substr(i2.fe_contab, 4, 2) || '-' || substr(i2.fe_contab, 1, 2) DESC, i2.hora DESC
                        LIMIT 1
                    ) as precio_unitario
                FROM inventory_movements
                WHERE cmv = '201'
                  AND UPPER(TRIM(material)) IN ({placeholders})
                  AND fe_contab LIKE :year
                GROUP BY material, area_negocio
                ORDER BY material ASC, costo_total DESC
            """
            params["month"] = f"%{current_month_str}"
            params["year"] = f"%{current_year_str}"
            df = pd.read_sql(text(query), self.session.connection(), params=params)
            df = df.astype(object).where(pd.notnull(df), None)
    
            return {"data": df.to_dict(orient="records")}
        except Exception as e:
            logger.error(f"Error fetching consumos for Materiales: {e}")
            raise

    def get_material_trend(self, material: str, area_negocio: str, ceco: str) -> dict:
        material_clean = material.strip().upper()
        area_clean = area_negocio.strip()
    
        try:
            ceco_clean = ceco.strip().upper() if ceco else ""
            if ceco_clean:
                area_filter_sql = "UPPER(TRIM(ce_coste)) = :ceco"
                area_param = {"ceco": ceco_clean}
            else:
                area_filter_sql = """COALESCE((
                    SELECT MAX(area_negocio)
                    FROM outbound_deliveries o
                    WHERE UPPER(TRIM(o.centro_costo)) = UPPER(TRIM(inventory_movements.ce_coste))
                      AND o.area_negocio IS NOT NULL
                      AND TRIM(o.area_negocio) != ''
                ), 'SIN AREA') = :area"""
                area_param = {"area": area_clean}
    
            current_year = str(datetime.now().year)
    
            query = f"""
                SELECT
                    substr(fe_contab, 7, 4) || '-' || substr(fe_contab, 4, 2) as mes_orden,
                    substr(fe_contab, 4, 2) || '/' || substr(fe_contab, 7, 4) as mes_label,
                    SUM(cantidad) * -1 as cantidad,
                    SUM(importe_ml) * -1 as costo
                FROM inventory_movements
                WHERE cmv = '201'
                  AND UPPER(TRIM(material)) = :material
                  AND fe_contab LIKE :year
                  AND {area_filter_sql}
                GROUP BY mes_orden, mes_label
                ORDER BY mes_orden ASC
            """
            params = {"material": material_clean, "year": f"%{current_year}", **area_param}
            df = pd.read_sql(text(query), self.session.connection(), params=params)
            df = df.astype(object).where(pd.notnull(df), None)
    
            price_query = """
                SELECT (importe_ml / cantidad) as precio_unitario
                FROM inventory_movements
                WHERE UPPER(TRIM(material)) = :material 
                  AND cantidad != 0 
                  AND cmv = '201'
                ORDER BY substr(fe_contab, 7, 4) || '-' || substr(fe_contab, 4, 2) || '-' || substr(fe_contab, 1, 2) DESC, hora DESC
                LIMIT 1
            """
            precio_unitario_row = self.session.connection().execute(text(price_query), {"material": material_clean}).fetchone()
            precio_unitario = abs(float(precio_unitario_row[0])) if precio_unitario_row and precio_unitario_row[0] is not None else 0
    
            return {
                "material": material,
                "area_negocio": area_negocio,
                "precio_unitario": precio_unitario,
                "current_year": current_year,
                "labels": df["mes_label"].tolist(),
                "cantidad": [float(v) if v is not None else 0 for v in df["cantidad"].tolist()],
                "costo": [float(v) if v is not None else 0 for v in df["costo"].tolist()]
            }
        except Exception as e:
            logger.error(f"Error fetching trend for material {material}: {e}")
            raise

    def check_table_exists(self) -> bool:
        try:
            res = self.session.execute(text("SELECT 1 FROM sqlite_master WHERE type='table' AND name='inventory_movements'")).scalar()
            return bool(res)
        except Exception:
            return False
