import pytest
from sqlalchemy.exc import OperationalError
from app.db.session import get_db

def test_db_connection():
    try:
        # Intenta abrir y cerrar una sesión con la base de datos
        with get_db() as _:
            pass
    except OperationalError as e:
        pytest.fail(f"La conexión a la base de datos falló: {str(e)}")
    except Exception as e:
        pytest.fail(f"Ocurrió un error inesperado: {str(e)}")