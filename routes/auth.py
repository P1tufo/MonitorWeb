"""
routes/auth.py — Endpoints de autenticación y gestión de usuarios (Pilar 6).

Endpoints:
  POST /api/auth/login    — Login con username/password, retorna JWT.
  POST /api/auth/register — Crear nuevo usuario (solo admin).
  GET  /api/auth/me       — Info del usuario autenticado.
  GET  /api/auth/users    — Listar usuarios (solo admin).
  GET  /login             — Vista HTML del formulario de login.
"""
import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Request, Response, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.database import get_session_dep
from core.models_auth import User
from core.auth import (
    hash_password, verify_password,
    create_access_token, require_auth, require_admin,
    get_current_user,
    TokenResponse, UserCreate, UserPublic,
)
from core.app_instance import templates
from core.state import AppState, get_app_state

logger = logging.getLogger("routes-auth")
router = APIRouter()

DBSession = Annotated[Session, Depends(get_session_dep)]


# ─── Login ─────────────────────────────────────────────────────────────────────
@router.post("/api/auth/login", response_model=TokenResponse)
def login(
    response: Response,
    form: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_session_dep)
):
    """
    Autentica un usuario con username/password y retorna un JWT.
    Compatible con el flujo OAuth2 de FastAPI (form-data).
    """
    user = db.query(User).filter(User.username == form.username).first()

    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cuenta desactivada. Contacte al administrador.",
        )

    token, expires_in = create_access_token(user.username, user.role)
    logger.info(f"Login exitoso: {user.username} (role={user.role})")

    # Establecer cookie de SESIÓN para navegación SSR
    # Al no poner max_age ni expires, el navegador la borra al cerrarse.
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False, # Cambiar a True en producción con HTTPS
        path="/",
    )

    return TokenResponse(
        access_token=token,
        expires_in=expires_in,
        username=user.username,
        role=user.role,
    )


@router.post("/api/auth/logout")
def logout(response: Response, state: AppState = Depends(get_app_state)):
    """Limpia la cookie de autenticación."""
    response.delete_cookie("access_token", path="/")
    return {"status": "success", "message": "Sesión cerrada"}



# ─── Perfil del usuario autenticado ───────────────────────────────────────────
@router.get("/api/auth/me")
def get_me(user: User = Depends(require_auth), state: AppState = Depends(get_app_state)):
    """Retorna la información del usuario autenticado."""
    return {
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": str(user.created_at),
    }


# ─── Registro de usuarios (solo admin) ────────────────────────────────────────
@router.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
def register_user(data: UserCreate, db: DBSession, admin: User = Depends(require_admin), state: AppState = Depends(get_app_state)):
    """Crea un nuevo usuario. Solo accesible por administradores."""
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(status_code=409, detail="El usuario ya existe")

    if data.role not in ("admin", "viewer"):
        raise HTTPException(status_code=400, detail="Rol inválido. Usar 'admin' o 'viewer'.")

    new_user = User(
        username=data.username,
        password_hash=hash_password(data.password),
        role=data.role,
    )
    db.add(new_user)
    db.flush()
    logger.info(f"Nuevo usuario creado por {admin.username}: {data.username} (role={data.role})")

    return {"status": "success", "message": f"Usuario '{data.username}' creado", "id": new_user.id}


# ─── Listar usuarios (solo admin) ─────────────────────────────────────────────
@router.get("/api/auth/users")
def list_users(db: DBSession, admin: User = Depends(require_admin), state: AppState = Depends(get_app_state)):
    """Lista todos los usuarios del sistema."""
    users = db.query(User).all()
    return [
        {
            "id": u.id,
            "username": u.username,
            "role": u.role,
            "is_active": u.is_active,
            "created_at": str(u.created_at),
        }
        for u in users
    ]


# ─── Vista HTML: Login ─────────────────────────────────────────────────────────
@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, state: AppState = Depends(get_app_state)):
    """Renderiza la página de login."""
    return templates.TemplateResponse(request=request, name="login.html", context={"request": request})
