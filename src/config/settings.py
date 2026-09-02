import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENV_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ENV_ROOT / ".env")


DATA_DIR = PROJECT_ROOT / "prueba-data-engineer"
RAW_DIR = DATA_DIR / "data/raw"
RAW_FILE_1 = RAW_DIR / "2012-1.csv"
RAW_FILE_2 = RAW_DIR / "2012-2.csv"
RAW_FILE_3 = RAW_DIR / "2012-3.csv"
RAW_FILE_4 = RAW_DIR / "2012-4.csv"
RAW_FILE_5 = RAW_DIR / "2012-5.csv"
RAW_FILE_VALIDATION = RAW_DIR / "validation"

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "prueba_data_engineer")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_SCHEMA = os.getenv("POSTGRES_SCHEMA", "public")
POSTGRES_TABLE = os.getenv("POSTGRES_TABLE", "transactions")
POSTGRES_TABLE_STATS = os.getenv("POSTGRES_TABLE", "pipeline_stats")
