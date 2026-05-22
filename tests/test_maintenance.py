import pytest
import subprocess
from unittest.mock import patch, MagicMock
from scripts.free_ram import quit_app
from scripts.doc_generator import should_process

def test_quit_app_success() -> None:
    """Verifica que quit_app retorne True cuando el comando de sistema tiene éxito."""
    # Usamos patch directo sobre el módulo para asegurar aislamiento en este contexto
    with patch("subprocess.run") as mock_run:
        # Simular un objeto CompletedProcess exitoso
        mock_run.return_value = MagicMock(spec=subprocess.CompletedProcess, returncode=0)
        
        app_name = "TestApp"
        result = quit_app(app_name)
        
        assert result is True, f"quit_app debería haber retornado True para la aplicación {app_name}"
        mock_run.assert_called_once()
        # Verificar que se intentó cerrar la aplicación correcta inspeccionando la lista de argumentos
        args, _ = mock_run.call_args
        command_list = args[0]
        assert any(app_name in arg for arg in command_list), f"El nombre de la app '{app_name}' no se encontró en el comando: {command_list}"

def test_quit_app_failure() -> None:
    """Verifica que quit_app retorne False cuando ocurre un error de proceso o excepción."""
    # Caso 1: Error de proceso (CalledProcessError)
    with patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "osascript")):
        assert quit_app("NonExistentApp") is False, "Debería retornar False si el comando falla"

    # Caso 2: Excepción genérica de sistema
    with patch("subprocess.run", side_effect=RuntimeError("Fallo de sistema")):
        assert quit_app("AnyApp") is False, "Debería retornar False ante excepciones de tiempo de ejecución"

@pytest.mark.parametrize("filename, filepath, expected", [
    ("app.py", "./app.py", True),
    ("dashboard.js", "./static/js/dashboard.js", True),
    ("index.js", "./node_modules/index.js", False),
    (".gitconfig", "./.git/config", False),
    ("package.json", "./package.json", False),
    ("manual.pdf", "./docs/manual.pdf", False),
    (".env", "./.env", False),
])
def test_doc_generator_filtering_logic(filename: str, filepath: str, expected: bool) -> None:
    """
    Prueba la lógica de exclusión de archivos en el generador de documentación
    utilizando parametrización para evitar duplicidad y mejorar la legibilidad.
    """
    assert should_process(filename, filepath, {}) is expected, f"Error en la lógica de filtrado para {filepath}"
