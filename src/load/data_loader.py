import logging

import pandas as pd
from sqlalchemy import text

from src.config.settings import POSTGRES_SCHEMA, POSTGRES_TABLE, POSTGRES_TABLE_STATS
from src.load.db_connector import create_postgres_engine

logger = logging.getLogger(__name__)


def load_transactions_to_postgres(df: pd.DataFrame) -> None:
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


def update_stats_accumulator(new_stats: pd.DataFrame) -> None:
    """Actualiza o inserta acumuladores de estadísticas en PostgreSQL.

    Args:
        new_stats: DataFrame con total_rows, price_sum, price_min, price_max.

    Raises:
        Exception: Cualquier error se registra en el log y se relanza.
    """
    logger.info("Actualizando acumuladores de estadísticas en PostgreSQL")

    try:
        engine = create_postgres_engine()

        with engine.connect() as conn:
            # Crear tabla si no existe
            conn.execute(text(f"""
                    CREATE TABLE IF NOT EXISTS {POSTGRES_SCHEMA}.{POSTGRES_TABLE_STATS} (
                        total_rows INTEGER DEFAULT 0,
                        price_sum NUMERIC DEFAULT 0,
                        price_min NUMERIC,
                        price_max NUMERIC
                    )
                """))

            new_rows = int(new_stats["total_rows"].iloc[0])
            new_sum = (
                float(new_stats["price_sum"].iloc[0])
                if pd.notna(new_stats["price_sum"].iloc[0])
                else None
            )
            new_min = (
                float(new_stats["price_min"].iloc[0])
                if pd.notna(new_stats["price_min"].iloc[0])
                else None
            )
            new_max = (
                float(new_stats["price_max"].iloc[0])
                if pd.notna(new_stats["price_max"].iloc[0])
                else None
            )

            # Verificar si existe al menos una fila
            result = conn.execute(
                text(f"SELECT COUNT(*) FROM {POSTGRES_SCHEMA}.{POSTGRES_TABLE_STATS}")
            )
            count = result.scalar()

            if count > 0:
                # UPDATE
                conn.execute(
                    text(f"""
                        UPDATE {POSTGRES_SCHEMA}.{POSTGRES_TABLE_STATS}
                        SET 
                            total_rows = total_rows + :p_total_rows,
                            price_sum = COALESCE(price_sum, 0) + COALESCE(:p_price_sum, 0),
                            price_min = CASE 
                                WHEN price_min IS NULL THEN :p_price_min
                                WHEN :p_price_min IS NULL THEN price_min
                                ELSE LEAST(price_min, :p_price_min)
                            END,
                            price_max = CASE 
                                WHEN price_max IS NULL THEN :p_price_max
                                WHEN :p_price_max IS NULL THEN price_max
                                ELSE GREATEST(price_max, :p_price_max)
                            END
                    """),
                    {
                        "p_total_rows": new_rows,
                        "p_price_sum": new_sum,
                        "p_price_min": new_min,
                        "p_price_max": new_max,
                    },
                )
            else:
                # INSERT
                conn.execute(
                    text(f"""
                        INSERT INTO {POSTGRES_SCHEMA}.{POSTGRES_TABLE_STATS} 
                            (total_rows, price_sum, price_min, price_max)
                        VALUES (:p_total_rows, COALESCE(:p_price_sum, 0), :p_price_min, :p_price_max)
                    """),
                    {
                        "p_total_rows": new_rows,
                        "p_price_sum": new_sum,
                        "p_price_min": new_min,
                        "p_price_max": new_max,
                    },
                )
            conn.commit()

        logger.info(
            "Acumuladores actualizados/insertados en '%s.%s'",
            POSTGRES_SCHEMA,
            POSTGRES_TABLE_STATS,
        )

    except Exception:
        logger.exception("Error al actualizar acumuladores de estadísticas")
        raise
