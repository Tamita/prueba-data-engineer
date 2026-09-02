import logging

import pandas as pd

logger = logging.getLogger(__name__)


def parse_str_date_to_date_type(df_to_transform: pd.DataFrame) -> pd.DataFrame:
    """Convierte la columna 'timestamp' de string a datetime64.

    Args:
        df_to_transform: DataFrame con una columna 'timestamp' de tipo string.

    Returns:
        DataFrame con 'timestamp' convertido a datetime64[ns].

    Raises:
        ValueError: Si falta la columna 'timestamp'.
        Exception: Cualquier error de conversión se registra en el log y se relanza.
    """
    logger.info("Iniciando conversión de timestamp a datetime")

    try:
        if "timestamp" not in df_to_transform.columns:
            logger.error("No se encontró la columna 'timestamp' en el DataFrame")
            raise ValueError("No se encontró la columna 'timestamp' en el DataFrame")

        df_transformed = df_to_transform.copy()
        df_transformed["timestamp"] = pd.to_datetime(
            df_transformed["timestamp"],
            errors="coerce",
        )

        null_timestamps = df_transformed["timestamp"].isna().sum()
        if null_timestamps > 0:
            logger.warning(
                "Se encontraron %s timestamps nulos después de la conversión (posibles fechas inválidas)",
                null_timestamps,
            )

        logger.info(
            "Conversión de timestamp completada. Dtype: %s",
            df_transformed["timestamp"].dtype,
        )
        return df_transformed

    except Exception:
        logger.exception("Error al convertir la columna timestamp a datetime")
        raise


def add_source_file_column(
    df_to_transform: pd.DataFrame, source_file_name: str
) -> pd.DataFrame:
    """Agrega una columna 'source_file' con el nombre del archivo de origen.

    Args:
        df_to_transform: DataFrame al que se le agregará la columna.
        source_file_name: Nombre del archivo de origen (ej. '2012-1.csv').

    Returns:
        DataFrame con la nueva columna 'source_file'.

    Raises:
        ValueError: Si source_file_name está vacío o es None.
        Exception: Cualquier error se registra en el log y se relanza.
    """
    logger.info("Agregando columna source_file con valor: %s", source_file_name)

    try:
        if not source_file_name:
            logger.error("source_file_name está vacío o es None")
            raise ValueError("source_file_name no puede estar vacío o ser None")

        df_transformed = df_to_transform.copy()
        df_transformed["source_file"] = source_file_name

        logger.info(
            "Columna source_file agregada. Forma del DataFrame: %s",
            df_transformed.shape,
        )
        return df_transformed

    except Exception:
        logger.exception("Error al agregar la columna source_file")
        raise


def transform_dataframe(
    df_to_transform: pd.DataFrame, source_file_name: str
) -> pd.DataFrame:
    """Aplica todas las transformaciones al DataFrame.

    Esta función orquesta:
    1. Agregar la columna source_file.
    2. Convertir timestamp de string a datetime.

    Args:
        df_to_transform: DataFrame crudo proveniente del CSV.
        source_file_name: Nombre del archivo de origen.

    Returns:
        DataFrame transformado, listo para cargarse a PostgreSQL.

    Raises:
        Exception: Cualquier error de transformación se registra en el log y se relanza.
    """
    logger.info("Iniciando pipeline de transformación del DataFrame")

    try:
        df_transformed = add_source_file_column(df_to_transform, source_file_name)
        df_transformed = parse_str_date_to_date_type(df_transformed)

        logger.info(
            "Pipeline de transformación completado. Forma final: %s, columnas: %s",
            df_transformed.shape,
            list(df_transformed.columns),
        )
        return df_transformed

    except Exception:
        logger.exception(
            "Error al completar el pipeline de transformación del DataFrame"
        )
        raise
