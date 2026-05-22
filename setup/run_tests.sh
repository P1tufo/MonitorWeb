#!/bin/bash
# run_tests.sh — Script para ejecución simplificada de la suite de pruebas.


echo "--- MonitorWeb: Iniciando Suite de Pruebas ---"
echo "Entorno: Pytest + SQLite In-Memory"

# Ejecutar pytest con reporte detallado
pytest tests/ -vv --disable-warnings

if [ $? -eq 0 ]; then
    echo -e "\n[OK] Todas las pruebas pasaron correctamente."
else
    echo -e "\n[ERROR] Se detectaron fallos en la suite de pruebas."
    exit 1
fi
