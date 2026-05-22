from pathlib import Path
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from config import BASE_DIR

# Configuración de Identidad de la Aplicación
app: FastAPI = FastAPI(
    title="MonitorWeb Analytics",
    description="Plataforma de análisis y seguimiento de transacciones WMS.",
    version="2.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuración de Plantillas con Seguridad Reforzada
# Se utiliza Path para mayor robustez y se activa autoescape para prevenir ataques XSS.
templates_path = Path(BASE_DIR) / "templates"
templates: Jinja2Templates = Jinja2Templates(
    directory=str(templates_path)
)
