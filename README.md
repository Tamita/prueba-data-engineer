# prueba-data-engineer
Pipeline para desarrollar el ejercicio de acercamiento al cargo de la empresa Pragma para el rol de data engineer, es un pipeline que procesa chunks de archivos csv

## Requerimientos

- Python **3.12+** (Ver `pyproject.toml`)
- [Poetry](https://python-poetry.org/) Para dependencias
- [PostgreSQL](https://www.postgresql.org/) base de datos `.env`
- [GNU Make](https://www.gnu.org/software/make/) (validaciones de formato, limpieza, calidad; wraps Poetry)

## Instalación

```bash
poetry install
cp .env.example .env
# Editar .env con tu informacion de PostgreSQL host, database name, user, y password.
```

## Variable de entorno

| Variable | Descripcion | Valor por defecto |
|----------|-------------|---------|
| `POSTGRES_HOST` | Database host | `localhost` |
| `POSTGRES_PORT` | Database port | `5432` |
| `POSTGRES_DB` | Database name | `job_postings` |
| `POSTGRES_USER` | Database user | `postgres` |
| `POSTGRES_PASSWORD` | Database password | `postgres` |
| `POSTGRES_SCHEMA` | Schema for the raw load table | `public` |
| `POSTGRES_TABLE` | Raw staging table name | `raw_jobs` |

`.env` esta cargado en el repositorio raíz **prueba-data-engineer** (see `src/config/settings.py`).

## Comandos comunes

| Comando | Descripción |
|---------|-------------|
| `make help` | Lista los targets del Makefile y una breve descripción. |
| `make install` | Instala las dependencias con Poetry. |
| `make run` | Ejecuta el pipeline completo (`poetry run python -m src.main`). |
| `make fix` | Aplica formato con Black y auto-correcciones de Ruff en `src/` y `tests/` (modifica archivos). |
| `make qa` | Puerta de calidad: Black `--check`, Ruff, Mypy y pytest (sin escribir cambios de formato). |
| `make test` | Ejecuta pytest con salida verbose. |
| `make test-cov` | Ejecuta las pruebas con un reporte de cobertura. |


## Git branching

- `main` — rama principal.
- `development` — rama de integración.
- Nomenclatura de ramas: `scope/description`, por ejemplo `feature/...`, `bugfix/...`, `docs/...`, `test/...`.


## Herramientas Desarrollo

- **pytest** — tests  
- **ruff** — lint (`make lint`, auto-fix via `make lint-fix` / `make fix`)  
- **black** — format (`make format`, check via `make format-check` / `make qa`)  
- **mypy** — static types (`make type-check` / `make qa`)

## Estructura de directorios del proyecto

```text
src/
  config/       # Configuración respaldada por variables de entorno.
  extract/      # Ingesta de archivos CSV.
  transform/    # Parsing y validación.
  load/         # Carga cruda, bootstrap de la base de datos y ejecución de SQL de normalización.
    sql/        # Scripts DDL normalizados y scripts semilla.
  utils/        # Utilidades de logging y funciones compartidas.
tests/          # Pruebas.
```
