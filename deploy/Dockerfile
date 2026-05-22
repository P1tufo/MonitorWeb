# ─────────────────────────────────────────────────────────────────────────────
# MonitorWeb — Dockerfile Multi-Stage (Producción SaaS)
# ─────────────────────────────────────────────────────────────────────────────
# Stage 1: Builder — instala dependencias en una imagen pesada.
# Stage 2: Runtime — imagen slim final sin compiladores ni caché de pip.
# Resultado: imagen ~60% más liviana y sin herramientas de ataque.
# ─────────────────────────────────────────────────────────────────────────────

# ── Stage 1: Builder ──────────────────────────────────────────────────────────
FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

# Dependencias del sistema para compilar paquetes nativos (numpy, pandas, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python en un directorio aislado
COPY setup/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Stage 2: Runtime ──────────────────────────────────────────────────────────
FROM python:3.13-slim AS runtime

# Metadatos de la imagen
LABEL maintainer="MonitorWeb SaaS Team" \
      description="MonitorWeb — Plataforma de Analíticas WMS-Agnóstica" \
      version="2.0.0"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Variables de configuración para Docker (sobreescribibles via docker-compose)
    APP_HOST=0.0.0.0 \
    APP_PORT=8000 \
    APP_RELOAD=false \
    # Base de datos: SQLite por defecto, PostgreSQL via DATABASE_URL
    DB_PATH=/app/data/wms_transactions.db

WORKDIR /app

# Copiar las dependencias pre-compiladas desde el builder
COPY --from=builder /install /usr/local

# Copiar el código fuente de la aplicación
COPY . /app

# Crear directorios de datos persistentes
RUN mkdir -p /app/data /app/PDFs_Generados /app/Temp_Assets /app/DELIVERIES_cleansed

# Puerto de la aplicación
EXPOSE 8000

# Healthcheck: verifica que la API responda cada 30s
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/status')" || exit 1

# Comando de producción: Uvicorn sin reload, con workers configurables
CMD ["python", "main.py"]
