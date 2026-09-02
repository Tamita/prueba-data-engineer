#!/usr/bin/env python3
"""Script para ejecutar el pipeline completo con todos los archivos."""

import logging
import subprocess
from pathlib import Path

from sqlalchemy import create_engine, text
from src.config.settings import (
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB,
    RAW_FILE_1,
    RAW_FILE_2,
    RAW_FILE_3,
    RAW_FILE_4,
    RAW_FILE_5,
    RAW_FILE_VALIDATION,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def get_db_engine():
    """Crea un engine de SQLAlchemy para PostgreSQL."""
    return create_engine(
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )


def show_pipeline_stats(engine):
    """Muestra estadísticas de pipeline_stats."""
    logger.info("=" * 50)
    logger.info("Estadísticas de pipeline_stats:")
    logger.info("=" * 50)

    with engine.connect() as conn:
        result = conn.execute(text("""
                SELECT 
                    total_rows,
                    price_sum,
                    price_min,
                    price_max,
                    CASE 
                        WHEN total_rows > 0 THEN ROUND((price_sum / total_rows)::NUMERIC, 2)
                        ELSE NULL 
                    END AS price_avg
                FROM public.pipeline_stats
            """))
        row = result.fetchone()
        if row:
            logger.info(f"total_rows: {row.total_rows}")
            logger.info(f"price_sum: {row.price_sum}")
            logger.info(f"price_min: {row.price_min}")
            logger.info(f"price_max: {row.price_max}")
            logger.info(f"price_avg: {row.price_avg}")
        else:
            logger.info("No hay datos en pipeline_stats")

    logger.info("")


def show_transactions_stats(engine):
    """Muestra estadísticas de transactions."""
    logger.info("=" * 50)
    logger.info("Estadísticas de transactions:")
    logger.info("=" * 50)

    with engine.connect() as conn:
        result = conn.execute(text("""
                SELECT 
                    COUNT(*) AS total,
                    SUM(price) as sum_price,
                    MIN(price) AS min_price,
                    MAX(price) AS max_price,
                    ROUND(AVG(price)::NUMERIC, 2) AS average_price
                FROM public.transactions
            """))
        row = result.fetchone()
        if row:
            logger.info(f"total: {row.total}")
            logger.info(f"sum_price: {row.sum_price}")
            logger.info(f"min_price: {row.min_price}")
            logger.info(f"max_price: {row.max_price}")
            logger.info(f"average_price: {row.average_price}")
        else:
            logger.info("No hay datos en transactions")

    logger.info("")


def run_pipeline(file_path: Path):
    """Ejecuta el pipeline para un archivo específico."""
    logger.info(f"Ejecutando pipeline para: {file_path}")
    logger.info("")

    subprocess.run(
        ["python", "-m", "src.main", str(file_path)],
        check=True,
    )

    logger.info("")


def main():
    """Ejecuta el pipeline completo."""
    logger.info("=" * 50)
    logger.info("Inicio del pipeline completo")
    logger.info("=" * 50)
    logger.info("")

    engine = get_db_engine()

    # 1. Mostrar estadísticas iniciales
    logger.info("1. Estadísticas iniciales de pipeline_stats:")
    show_pipeline_stats(engine)

    # 2. Ejecutar pipeline con cada archivo de datos
    logger.info("2. Ejecutando pipeline para archivos de datos:")
    logger.info("")

    data_files = [
        RAW_FILE_1,
        RAW_FILE_2,
        RAW_FILE_3,
        RAW_FILE_4,
        RAW_FILE_5,
    ]

    for file_path in data_files:
        run_pipeline(file_path)

    # 3. Mostrar estadísticas después de cargar datos
    logger.info("3. Estadísticas de pipeline_stats después de cargar datos:")
    show_pipeline_stats(engine)

    # 4. Ejecutar pipeline con archivo de validación
    logger.info("4. Ejecutando pipeline para archivo de validación:")
    logger.info("")
    run_pipeline(RAW_FILE_VALIDATION)

    # 5. Mostrar estadísticas finales de pipeline_stats
    logger.info("5. Estadísticas finales de pipeline_stats:")
    show_pipeline_stats(engine)

    # 6. Mostrar estadísticas de transactions
    logger.info("6. Estadísticas de transactions:")
    show_transactions_stats(engine)

    logger.info("=" * 50)
    logger.info("Pipeline completo finalizado")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()
