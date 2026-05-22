import pytest
from core.utils import setup_signal_handlers

def test_setup_signal_handlers_safety() -> None:
    """
    Verifica que el registro de manejadores de señales sea seguro e idempotente.
    Asegura que llamadas repetidas no provoquen excepciones en el sistema de señales.
    """
    # El registro de señales no debe lanzar excepciones críticas.
    # Se valida la ejecución exitosa de la rutina de configuración.
    setup_signal_handlers()
    setup_signal_handlers()
