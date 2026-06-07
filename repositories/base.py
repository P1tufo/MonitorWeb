from sqlalchemy.orm import Session

from core.db_config_manager import get_query_visual_state


class BaseRepository:
    """Clase base para todos los repositorios de datos."""

    def __init__(self, session: Session):
        self.session = session

    def _sql(self, query_id: str, fallback: str) -> str:
        """
        Devuelve el fallback hardcodeado. (Fase 4 completada: sql_text ha sido eliminado).
        """
        return fallback

    def _has_visual_state(self, query_id: str) -> bool:
        """
        Retorna True si la query tiene un visual_state JSON almacenado.
        """
        return bool(get_query_visual_state(query_id))
