import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def read_raw_csv(file_path: Path) -> pd.DataFrame:
    """Carga el dataset crudo desde un CSV a un DataFrame de pandas.

    Args:
        file_path: Ruta al archivo CSV.

    Returns:
        DataFrame con una fila por cada vacante.

    Raises:
        Exception: Cualquier error de ``pandas.read_csv`` se registra en el log y se relanza.
    """
    logger.info("Iniciando lectura del CSV desde %s", file_path)

    try:
        df = pd.read_csv(file_path)
        logger.info(
            "CSV cargado exitosamente con %s filas y %s columnas",
            len(df),
            len(df.columns),
        )
        return df
    except Exception:
        logger.exception("Error al leer el CSV crudo desde %s", file_path)
        raise
