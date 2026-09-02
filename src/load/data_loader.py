import logging

import pandas as pd

from src.config.settings import POSTGRES_SCHEMA, POSTGRES_TABLE
from src.load.db_connector import create_postgres_engine

logger = logging.getLogger(__name__)


def load_to_postgres(df: pd.DataFrame) -> None:
    """Reemplaza la tabla configurada en PostgreSQL con el contenido de ``df``.

    Usa ``if_exists='replace'`` y mapea las columnas anidadas al tipo ``JSON``
    de SQLAlchemy donde esté configurado. El esquema y la tabla vienen de settings.

    Args:
        df: DataFrame validado después del parseo.

    Raises:
        Exception: Los errores de base de datos o de ``to_sql`` de pandas se
            registran en el log y se relanzan.
    """
    logger.info(
        "Iniciando carga a PostgreSQL para la tabla '%s.%s'",
        POSTGRES_SCHEMA,
        POSTGRES_TABLE,
    )

    try:
        engine = create_postgres_engine()

        df.to_sql(
            name=POSTGRES_TABLE,
            con=engine,
            schema=POSTGRES_SCHEMA,
            if_exists="append",
            index=False,
        )

        logger.info(
            "Carga a PostgreSQL completada exitosamente para la tabla '%s.%s'",
            POSTGRES_SCHEMA,
            POSTGRES_TABLE,
        )
    except Exception:
        logger.exception(
            "Error al cargar el DataFrame en la tabla de PostgreSQL '%s.%s'",
            POSTGRES_SCHEMA,
            POSTGRES_TABLE,
        )
        raise
