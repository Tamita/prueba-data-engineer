import logging

import psycopg
from psycopg import sql

from src.config.settings import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)

logger = logging.getLogger(__name__)


def ensure_database_exists() -> None:
    """Crea ``POSTGRES_DB`` si todavía no existe.

    Se conecta a la base de mantenimiento ``postgres`` con ``autocommit=True``,
    revisa ``pg_database`` y ejecuta ``CREATE DATABASE`` cuando hace falta.
    """
    logger.info("Verificando si la base de datos PostgreSQL '%s' existe", POSTGRES_DB)

    conn = psycopg.connect(
        dbname="postgres",
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        autocommit=True,
    )

    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s",
                (POSTGRES_DB,),
            )
            exists = cur.fetchone()

            if exists:
                logger.info("La base de datos '%s' ya existe", POSTGRES_DB)
                return

            cur.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(POSTGRES_DB))
            )
            logger.info("Base de datos '%s' creada exitosamente", POSTGRES_DB)
    finally:
        conn.close()