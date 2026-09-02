import argparse
import logging
from pathlib import Path

from src.extract.data_extractor import read_raw_csv
from src.load.data_loader import load_transactions_to_postgres, update_stats_accumulator
from src.load.db_bootstrap import ensure_database_exists
from src.transform.data_transformer import get_stats_info, transform_dataframe
from src.utils.logging_config import setup_logging

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Pipeline de carga de datos a PostgreSQL"
    )
    parser.add_argument(
        "file_path",
        type=Path,
        help="Path al archivo CSV a procesar (ej: data/raw/2012-1.csv)",
    )
    return parser.parse_args()


def main() -> None:
    """Ejecuta el pipeline para 1 archivo csv."""
    args = parse_args()
    setup_logging()

    file_path = args.file_path
    logger.info("Archivo recibido como parámetro: %s", file_path)

    # Validar que el archivo existe
    if not file_path.exists():
        logger.error("El archivo no existe: %s", file_path)
        raise FileNotFoundError(f"El archivo no existe: {file_path}")

    logger.info("Inicio del pipeline")

    ensure_database_exists()
    df_raw = read_raw_csv(file_path)
    df_transformed = transform_dataframe(df_raw, source_file_name=file_path.name)
    df_statistics = get_stats_info(df_transformed)
    load_transactions_to_postgres(df_transformed)
    update_stats_accumulator(df_statistics)

    logger.info("Pipeline se ejecutó exitosamente")


if __name__ == "__main__":
    main()
