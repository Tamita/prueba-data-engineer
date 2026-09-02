# prueba-data-engineer
Pipeline para el ejercicio de acercamiento al cargo de Data Engineer en Pragma: procesa archivos CSV de transacciones y los carga en PostgreSQL.

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

## Datos de entrada

Los archivos CSV a procesar van en `data/raw/`. El proyecto viene configurado para trabajar con:

- `2012-1.csv` … `2012-5.csv` — archivos de datos.
- `validation.csv` — archivo de validación.

Las rutas están definidas en `src/config/settings.py`.

## Variables de entorno

| Variable | Descripción | Valor por defecto |
|----------|-------------|---------|
| `POSTGRES_HOST` | Host de la base de datos | `localhost` |
| `POSTGRES_PORT` | Puerto de la base de datos | `5432` |
| `POSTGRES_DB` | Nombre de la base de datos | `prueba_data_engineer` |
| `POSTGRES_USER` | Usuario de la base de datos | `postgres` |
| `POSTGRES_PASSWORD` | Contraseña de la base de datos | `postgres` |
| `POSTGRES_SCHEMA` | Esquema para las tablas de carga | `public` |
| `POSTGRES_TABLE` | Tabla de carga cruda por archivo | `transactions` |
| `POSTGRES_STATS_TABLE` | Tabla acumuladora de estadísticas | `pipeline_stats` |

`.env` está cargado en el repositorio raíz **prueba-data-engineer** (ver `src/config/settings.py`). La base de datos y su esquema se crean automáticamente al ejecutar el pipeline si no existen (ver `src/load/db_bootstrap.py`).

## Uso

Procesar un único archivo:

```bash
make run FILE=data/raw/2012-1.csv
```

Procesar el pipeline completo (los 5 archivos de datos, luego el de validación, mostrando las estadísticas acumuladas antes y después de cada etapa):

```bash
make run-full
```

## Tablas generadas

- **`transactions`** (`POSTGRES_TABLE`): tabla de staging con los datos transformados del archivo procesado más reciente. Se reemplaza (`if_exists='replace'`) en cada corrida individual del pipeline.
- **`pipeline_stats`** (`POSTGRES_STATS_TABLE`): acumulador incremental (`total_rows`, `price_sum`, `price_min`, `price_max`) que se actualiza —no se reemplaza— en cada corrida, sumando los datos del nuevo archivo a los ya cargados.

## Comandos comunes

| Comando | Descripción |
|---------|-------------|
| `make help` | Lista los targets del Makefile y una breve descripción. |
| `make install` | Instala las dependencias con Poetry. |
| `make run FILE=<ruta>` | Ejecuta el pipeline para un único archivo CSV. |
| `make run-full` | Ejecuta el pipeline completo sobre todos los archivos de `data/raw/`. |
| `make fix` | Aplica formato con Black y auto-correcciones de Ruff en `src/` y `tests/` (modifica archivos). |
| `make qa` | Puerta de calidad: Black `--check`, Ruff, Mypy y pytest (sin escribir cambios de formato). |
| `make test` | Ejecuta pytest con salida verbose. |
| `make test-cov` | Ejecuta las pruebas con un reporte de cobertura. |


## Git branching

- `main` — rama principal.
- `development` — rama de integración.
- Nomenclatura de ramas: `scope/description`, por ejemplo `feature/...`, `bugfix/...`, `docs/...`, `test/...`.


## Herramientas Desarrollo

- **pytest** — tests (aún sin casos escritos en `tests/`)
- **ruff** — lint (`make lint`, auto-fix via `make lint-fix` / `make fix`)
- **black** — format (`make format`, check via `make format-check` / `make qa`)
- **mypy** — static types (`make type-check` / `make qa`)

## Estructura de directorios del proyecto

```text
data/raw/       # CSVs de entrada (2012-1.csv … 2012-5.csv, validation.csv).
scripts/        # Orquestación del pipeline completo (run_full_files.py).
src/
  config/       # Configuración respaldada por variables de entorno.
  extract/      # Ingesta de archivos CSV.
  transform/    # Parsing, transformación y cálculo de estadísticas.
  load/         # Bootstrap de la base de datos, conexión y carga a PostgreSQL.
  utils/        # Configuración de logging.
tests/          # Pruebas.
```
