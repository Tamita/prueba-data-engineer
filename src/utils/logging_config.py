import logging
from pathlib import Path


def setup_logging() -> None:
    """Configura el logger raíz en nivel INFO hacia stderr y ``logs/pipeline.log``.

    Si el logger raíz ya tiene handlers configurados, no hace nada (evita logs
    duplicados cuando ``setup_logging`` se llama más de una vez).
    """
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    if root_logger.handlers:
        return

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(logs_dir / "pipeline.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
