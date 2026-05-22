"""
core/security.py — Utilidades centralizadas de seguridad y validación.
"""
from typing import Final, Set

# Lista blanca global de tablas permitidas para evitar SQL Injection
WHITELIST_TABLES: Final[Set[str]] = {
    "outbound_deliveries",
    "stock_levels",
    "inventory_movements",
    "warehouse_tasks"
}

def validate_table(table_name: str) -> None:
    """Valida el nombre de la tabla contra la lista blanca para prevenir SQL Injection."""
    if table_name not in WHITELIST_TABLES:
        raise ValueError(f"Intento de acceso a tabla no permitida: {table_name}")
