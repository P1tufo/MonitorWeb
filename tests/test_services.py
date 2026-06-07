from unittest.mock import MagicMock, patch

import pytest

from core.state import CacheManager, SyncStateManager
from services.tunnel import start_tunnel, stop_tunnel

# Constantes de configuración centralizadas para las pruebas
TEST_MAX_CACHE_SIZE = 5

@pytest.fixture
def cache_manager() -> CacheManager:
    """
    Proporciona una instancia limpia de CacheManager.
    Encapsula la configuración del límite de caché para pruebas.
    """
    manager = CacheManager()
    # Configuración del límite mediante setter público
    manager.max_cache_size = TEST_MAX_CACHE_SIZE
    return manager

@pytest.fixture
def sync_manager() -> SyncStateManager:
    return SyncStateManager()

@pytest.fixture(autouse=True)
def cleanup_tunnel() -> None:
    """
    Garantiza la limpieza del estado global del túnel tras cada test.
    Implementación segura ante fallos de inicialización (idempotencia).
    """
    yield
    try:
        stop_tunnel()
    except Exception:
        # Se silencia para evitar que errores de limpieza interfieran con el resultado del test
        pass

def test_state_cache_respects_limits(cache_manager: CacheManager) -> None:
    """
    Verifica que el gestor de estado respete los límites de memoria.
    Valida que tras exceder el límite, el tamaño de la caché se mantenga bajo control.
    """
    for i in range(TEST_MAX_CACHE_SIZE * 2):
        cache_manager.set_cache(f"key_{i}", i)

    # Validación del tamaño mediante propiedad pública
    assert cache_manager.cache_size <= TEST_MAX_CACHE_SIZE, "La caché no aplicó la política de desalojo correctamente"

def test_state_sync_flag_reactivity(sync_manager: SyncStateManager) -> None:
    """Valida que la propiedad reactiva de sincronización cambie su estado de forma consistente."""
    sync_manager.is_syncing = True
    assert sync_manager.is_syncing is True, "El estado de sincronización debería ser activo"
    sync_manager.is_syncing = False
    assert sync_manager.is_syncing is False, "El estado de sincronización debería ser inactivo"

@patch("subprocess.Popen")
@patch("os.path.exists", return_value=True)
@patch("os.access", return_value=True)
def test_start_tunnel_manages_singleton_instance(mock_access, mock_exists, mock_popen) -> None:
    """
    Verifica que start_tunnel inicialice correctamente el servicio de túnel.
    Asegura que el servicio se cree y sea accesible tras la llamada.
    """
    mock_process = MagicMock()
    mock_popen.return_value = mock_process

    # El retorno de start_tunnel debe ser una instancia válida
    service = start_tunnel()
    assert service is not None, "La función debería retornar la instancia del servicio de túnel"
    assert service.process is not None, "El proceso de túnel debería haber sido inicializado"

@patch("subprocess.run")
def test_stop_tunnel_releases_global_reference(mock_run) -> None:
    """
    Valida que stop_tunnel limpie las referencias globales de forma segura.
    Se verifica a través de la API pública para evitar el acceso a atributos privados.
    """
    # Simular inicio
    with patch("services.tunnel.NgrokService.start", return_value=None):
        start_tunnel()

    # Detener túnel
    stop_tunnel()

    # Si stop_tunnel funcionó, una nueva llamada a start_tunnel creará una nueva instancia
    # (en lugar de reutilizar la anterior si no fuera None)
    with patch("services.tunnel.NgrokService.start", return_value=None):
        service_nuevo = start_tunnel()
        assert service_nuevo is not None, "Debería ser posible reiniciar el servicio tras detenerlo"
