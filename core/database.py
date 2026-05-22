"""
core/database.py — Fábrica de sesiones SQLAlchemy (ORM Layer).

Este módulo es el punto de entrada único para acceder a la capa ORM.
Soporta SQLite (desarrollo local) y PostgreSQL (producción SaaS) via DATABASE_URL.

Uso:
    from core.database import get_session, engine

    with get_session() as session:
        records = session.query(StatusMapping).all()
"""
import os
import logging
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

from config import DB_PATH

logger = logging.getLogger("orm")

# ─── ENGINE ───────────────────────────────────────────────────────────────────
# La variable de entorno DATABASE_URL permite apuntar a cualquier BD compatible
# sin tocar código. En desarrollo usa SQLite local; en producción usa PostgreSQL.
#
# Ejemplos:
#   SQLite local (default):    sqlite:///./wms_transactions.db
#   PostgreSQL (SaaS prod):    postgresql+psycopg2://user:pass@host:5432/monitorweb
#
_DEFAULT_URL = f"sqlite:///{DB_PATH}"
DATABASE_URL = os.getenv("DATABASE_URL", _DEFAULT_URL)

# SQLite necesita check_same_thread=False para uso con FastAPI
_connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=_connect_args,
    # Pool de conexiones: ajustar en producción con PostgreSQL
    pool_pre_ping=True,   # Verifica que la conexión esté viva antes de usar
    echo=False,           # Cambiar a True para ver SQL generado en desarrollo
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,  # Evita lazy-loading sorpresivo tras commit
)


# ─── BASE DECLARATIVA ─────────────────────────────────────────────────────────
class Base(DeclarativeBase):
    """Clase base para todos los modelos ORM del sistema."""
    pass


# ─── CONTEXT MANAGER ──────────────────────────────────────────────────────────
@contextmanager
def get_session() -> Generator[Session, None, None]:
    """
    Context manager que entrega una sesión SQLAlchemy.
    Garantiza commit en éxito y rollback automático en excepción.

    Ejemplo:
        with get_session() as session:
            session.add(record)
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_session_dep() -> Generator[Session, None, None]:
    """
    Dependencia de FastAPI (Depends) para inyección de sesiones en endpoints.

    Ejemplo:
        @router.get("/items")
        def list_items(db: Session = Depends(get_session_dep)):
            ...
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def health_check() -> bool:
    """Verifica la conectividad con la base de datos. Retorna True si OK."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"DB health check failed: {e}")
        return False
