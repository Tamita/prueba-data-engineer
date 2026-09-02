import logging
from urllib.parse import quote_plus

from sqlalchemy import Engine, create_engine

from src.config.settings import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)

logger = logging.getLogger(__name__)


def build_postgres_connection_url() -> str:
    """Construye una URL de SQLAlchemy para ``postgresql+psycopg`` usando settings.

    Returns:
        Cadena de conexión con la contraseña codificada para caracteres especiales.
    """
    encoded_password = quote_plus(POSTGRES_PASSWORD)

    return (
        f"postgresql+psycopg://{POSTGRES_USER}:{encoded_password}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )


def create_postgres_engine() -> Engine:
    """Crea un nuevo ``Engine`` de SQLAlchemy para la base de datos PostgreSQL configurada.

    Returns:
        Engine construido a partir de ``build_postgres_connection_url()``.

    Raises:
        Exception: Los errores al crear el engine se registran en el log y se relanzan.
    """
    connection_url = build_postgres_connection_url()

    logger.info("Creando engine de PostgreSQL para la base de datos '%s'", POSTGRES_DB)

    try:
        engine = create_engine(connection_url)
        logger.info("Engine de PostgreSQL creado exitosamente")
        return engine
    except Exception:
        logger.exception("Error al crear el engine de PostgreSQL")
        raise
