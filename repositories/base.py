from sqlalchemy.orm import Session
from core.wms_config import get_query
from core.db_config_manager import get_query_visual_state

class BaseRepository:
    """Clase base para todos los repositorios de datos."""

    def __init__(self, session: Session):
        self.session = session

    def _sql(self, query_id: str, fallback: str) -> str:
        """
        Obtiene un SQL desde la BD de configuración, con fallback hardcodeado.

        ── Estado actual (Fase 1–2 del plan de migración) ───────────────────
        Intenta obtener sql_text de config_queries para el query_id dado.
        Si no existe sql_text (campo deprecado → nullable desde Fase 1) o
        está vacío, devuelve el `fallback` hardcodeado.

        ── Ruta de migración (Fase 3) ───────────────────────────────────────
        Este método será eliminado. Los repositorios derivados deberán:
          1. Llamar a get_query_visual_state(query_id) para obtener el JSON.
          2. Compilar el SQL via core/query_engine.build_sql_from_payload().
          3. Ejecutar con los bound_params devueltos por el motor.

        ── Nota de seguridad ─────────────────────────────────────────────────
        El SQL devuelto por este método proviene de config_queries, tabla
        que SOLO puede ser escrita por api_update_query (autenticado, admin).
        Desde Fase 1, ese endpoint solo acepta visual_state — el SQL en
        config_queries es compilado por core/query_engine y es parametrizado.
        El fallback es un literal hardcodeado en el repositorio derivado.
        ──────────────────────────────────────────────────────────────────────
        """
        from_db = get_query(query_id)
        return from_db if from_db else fallback

    def _has_visual_state(self, query_id: str) -> bool:
        """
        Retorna True si la query tiene un visual_state JSON almacenado.
        Útil para que los repositorios derivados detecten si deben migrar
        su lógica a core/query_engine en la Fase 3.
        """
        return bool(get_query_visual_state(query_id))
