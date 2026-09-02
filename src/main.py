import logging

from src.config.settings import (
    RAW_FILE_1,
)
from src.extract.data_extractor import read_raw_csv
from src.load.data_loader import load_transactions_to_postgres, load_stats_to_postgres
from src.load.db_bootstrap import ensure_database_exists
from src.transform.data_transformer import get_stats_info, transform_dataframe
from src.utils.logging_config import setup_logging

logger = logging.getLogger(__name__)


def main() -> None:
    """Ejecuta el pipeline para 1 archivo csv."""
    setup_logging()
    logger.info("Inicio del pipeline")

    ensure_database_exists()
    file_path = RAW_FILE_1
    df_raw = read_raw_csv(file_path)
    df_transformed = transform_dataframe(df_raw, source_file_name=file_path.name)
    df_statistics = get_stats_info(df_transformed)
    load_transactions_to_postgres(df_transformed)
    load_stats_to_postgres(df_statistics)

    # print(df_transformed)
    print(df_statistics)
    logger.info("Pipeline se ejecutó exitosamente")


if __name__ == "__main__":
    main()
