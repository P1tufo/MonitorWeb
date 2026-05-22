"""
core/auth.py — Autenticación y Seguridad JWT/OAuth2 (Pilar 6).

Arquitectura:
  - Modelo `User` en SQLAlchemy con password hasheado (bcrypt).
  - Tokens JWT con expiración configurable.
  - Dependencia FastAPI `get_current_user` para proteger endpoints.
  - Roles: 'admin' (acceso total), 'viewer' (solo lectura).

Uso:
    from core.auth import get_current_user, require_admin

    @router.get("/protected")
    def protected_route(user = Depends(get_current_user)):
        return {"hello": user.username}

    @router.post("/admin-only")
    def admin_route(user = Depends(require_admin)):
        ...
"""
import os
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, Annotated

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel

from .database import get_session_dep, engine, Base
from .models_auth import User

logger = logging.getLogger("auth")

# ─── Configuración JWT ────────────────────────────────────────────────────────
# SECRET_KEY: DEBE cambiarse en producción via variable de entorno.
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "monitorweb-dev-secret-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "480"))  # 8 horas

# Esquema OAuth2 de FastAPI (token via header Authorization: Bearer <token>)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

# Tipos reutilizables
DBSession = Annotated[Session, Depends(get_session_dep)]


# ─── Pydantic Schemas ─────────────────────────────────────────────────────────
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    username: str
    role: str

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "viewer"

class UserPublic(BaseModel):
    id: int
    username: str
    role: str
    is_active: bool
    created_at: str


# ─── Password Hashing ─────────────────────────────────────────────────────────
def hash_password(plain: str) -> str:
    """Genera un hash bcrypt del password."""
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain: str, hashed: str) -> bool:
    """Verifica un password contra su hash bcrypt."""
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


# ─── JWT Token Management ─────────────────────────────────────────────────────
def create_access_token(username: str, role: str) -> tuple[str, int]:
    """
    Crea un JWT firmado con HS256.
    Retorna (token_string, expires_in_seconds).
    """
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    payload = {
        "sub": username,
        "role": role,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token, int(expires_delta.total_seconds())

def decode_token(token: str) -> Optional[dict]:
    """Decodifica y valida un JWT. Retorna None si es inválido o expirado."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        logger.debug("Token expirado.")
        return None
    except jwt.InvalidTokenError as e:
        logger.debug(f"Token inválido: {e}")
        return None


# ─── Dependencias FastAPI ──────────────────────────────────────────────────────
def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    request: Request = None,
    db: Session = Depends(get_session_dep),
) -> User:
    """
    Dependencia que extrae el usuario del token JWT.
    Si no hay token, retorna un usuario 'invitado' con rol viewer.
    """
    # 1. Crear un usuario invitado por defecto (Guest)
    guest_user = User(username="invitado", role="viewer", is_active=True)
    actual_token = token
    if not actual_token and request:
        actual_token = request.cookies.get("access_token")

    if not actual_token:
        return guest_user

    payload = decode_token(actual_token)
    if not payload:
        return guest_user

    username = payload.get("sub")
    if not username:
        return guest_user

    user = db.query(User).filter(User.username == username, User.is_active == True).first()
    return user or guest_user

def require_auth(
    user: User = Depends(get_current_user),
) -> User:
    """Dependencia que EXIGE un usuario autenticado (no invitado)."""
    if user.username == "invitado":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticación requerida para esta acción",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def require_admin(
    user: User = Depends(require_auth),
) -> User:
    """Dependencia que EXIGE rol de administrador. Lanza 403 si no tiene permisos."""
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador",
        )
    return user


# ─── Inicialización ───────────────────────────────────────────────────────────
def init_auth_db():
    """Crea las tablas de autenticación si no existen."""
    Base.metadata.create_all(bind=engine)

def ensure_admin_exists():
    """
    Crea el usuario admin por defecto si no existe ningún usuario.
    Password por defecto: 'admin' — DEBE cambiarse en producción.
    """
    from .database import get_session
    with get_session() as session:
        if session.query(User).count() == 0:
            admin = User(
                username=os.getenv("ADMIN_USERNAME", "admin"),
                password_hash=hash_password(os.getenv("ADMIN_PASSWORD", "admin")),
                role="admin",
            )
            session.add(admin)
            logger.info("Usuario admin por defecto creado. CAMBIE la contraseña en producción.")
