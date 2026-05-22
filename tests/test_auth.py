"""
tests/test_auth.py — Tests de autenticación JWT (Pilar 6).
"""
import pytest
from fastapi.testclient import TestClient


def test_login_page_renders(client):
    """Verifica que la página de login sea accesible."""
    response = client.get("/login")
    assert response.status_code == 200
    assert "MonitorWeb" in response.text
    assert "username" in response.text


def test_login_success(client):
    """Verifica login exitoso con credenciales del admin por defecto."""
    response = client.post(
        "/api/auth/login",
        data={"username": "admin", "password": "admin"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["username"] == "admin"
    assert data["role"] == "admin"
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    """Verifica que credenciales incorrectas retornen 401."""
    response = client.post(
        "/api/auth/login",
        data={"username": "admin", "password": "wrong"},
    )
    assert response.status_code == 401


def test_me_endpoint_without_token(client):
    """Verifica que /me sin token retorne 401."""
    response = client.get("/api/auth/me")
    assert response.status_code == 401


def test_me_endpoint_with_token(client):
    """Verifica que /me con token válido retorne el perfil del usuario."""
    # 1. Login
    login_res = client.post(
        "/api/auth/login",
        data={"username": "admin", "password": "admin"},
    )
    token = login_res.json()["access_token"]

    # 2. Consultar perfil
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "admin"
    assert data["role"] == "admin"


def test_register_requires_admin(client):
    """Verifica que registrar un usuario requiera token de admin."""
    # Sin token → 401
    response = client.post(
        "/api/auth/register",
        json={"username": "new_user", "password": "pass123", "role": "viewer"},
    )
    assert response.status_code == 401


def test_register_and_login_new_user(client):
    """Verifica el flujo completo: admin registra usuario → nuevo usuario hace login."""
    # 1. Login como admin
    admin_res = client.post(
        "/api/auth/login",
        data={"username": "admin", "password": "admin"},
    )
    admin_token = admin_res.json()["access_token"]

    # 2. Registrar nuevo usuario
    reg_res = client.post(
        "/api/auth/register",
        json={"username": "viewer1", "password": "viewer123", "role": "viewer"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert reg_res.status_code == 201

    # 3. Login como nuevo usuario
    login_res = client.post(
        "/api/auth/login",
        data={"username": "viewer1", "password": "viewer123"},
    )
    assert login_res.status_code == 200
    assert login_res.json()["role"] == "viewer"


def test_list_users_admin_only(client):
    """Verifica que listar usuarios requiera rol admin."""
    # Login como admin
    login_res = client.post(
        "/api/auth/login",
        data={"username": "admin", "password": "admin"},
    )
    token = login_res.json()["access_token"]

    response = client.get(
        "/api/auth/users",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    users = response.json()
    assert len(users) >= 1
    assert any(u["username"] == "admin" for u in users)
