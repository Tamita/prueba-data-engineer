# Resultados de ejecución del pipeline completo

- **Comando:** `make run-full`
- **Fecha:** 2026-09-02 00:42
- **Rama:** `results`
- **Contexto:** ejecución realizada justo después de borrar las tablas `transactions` y `pipeline_stats` de la base `prueba_data_engineer`, para validar el pipeline desde cero.

## Resumen

| Paso | Descripción | Resultado |
|------|-------------|-----------|
| 1 | Estadísticas iniciales de `pipeline_stats` | Tabla no existía aún (sin datos) |
| 2 | Carga de los 5 archivos de datos | 143 filas cargadas en total |
| 3 | Estadísticas de `pipeline_stats` tras los 5 archivos | `total_rows=143`, `price_avg=56.27` |
| 4 | Carga del archivo de validación (`validation.csv`) | 8 filas cargadas |
| 5 | Estadísticas finales de `pipeline_stats` | `total_rows=151`, `price_avg=55.50` |
| 6 | Estadísticas de `transactions` | `total=151`, `average_price=57.01` |

## Detalle por archivo procesado

| Archivo | Filas | price_sum | price_min | price_max |
|---------|------:|----------:|----------:|----------:|
| `2012-1.csv` | 22 | 1193.0 | 14.0 | 97.0 |
| `2012-2.csv` | 29 | 1590 | 10 | 100 |
| `2012-3.csv` | 31 | 1850 | 12 | 99 |
| `2012-4.csv` | 30 | 1607.0 | 10.0 | 97.0 |
| `2012-5.csv` | 31 | 1806 | 13 | 100 |
| `validation.csv` | 8 | 334 | 11 | 92 |

## Estadísticas de `pipeline_stats` (acumulador incremental)

| Momento | total_rows | price_sum | price_min | price_max | price_avg |
|---------|-----------:|----------:|----------:|----------:|----------:|
| Inicial (antes de cargar) | — | — | — | — | — |
| Después de los 5 archivos de datos | 143 | 8046 | 10 | 100 | 56.27 |
| Final (después de validation.csv) | 151 | 8380 | 10 | 100 | 55.50 |

## Estadísticas de `transactions` (tabla de staging, estado final)

| total | sum_price | min_price | max_price | average_price |
|------:|----------:|----------:|----------:|---------------:|
| 151 | 8380.0 | 10.0 | 100.0 | 57.01 |

## Log completo de la ejecución

```text
2026-09-02 00:42:35,650 - __main__ - INFO - ==================================================
2026-09-02 00:42:35,650 - __main__ - INFO - Inicio del pipeline completo
2026-09-02 00:42:35,650 - __main__ - INFO - ==================================================
2026-09-02 00:42:35,650 - __main__ - INFO -
2026-09-02 00:42:35,683 - __main__ - INFO - 1. Estadísticas iniciales de pipeline_stats:
2026-09-02 00:42:35,683 - __main__ - INFO - ==================================================
2026-09-02 00:42:35,684 - __main__ - INFO - Estadísticas de pipeline_stats:
2026-09-02 00:42:35,684 - __main__ - INFO - ==================================================
2026-09-02 00:42:35,715 - __main__ - INFO - La tabla pipeline_stats aún no existe (sin datos)
2026-09-02 00:42:35,715 - __main__ - INFO -
2026-09-02 00:42:35,715 - __main__ - INFO - 2. Ejecutando pipeline para archivos de datos:
2026-09-02 00:42:35,715 - __main__ - INFO -
2026-09-02 00:42:35,715 - __main__ - INFO - Ejecutando pipeline para: /Users/tamita/development/pragma/prueba-data-engineer/data/raw/2012-1.csv
2026-09-02 00:42:35,715 - __main__ - INFO -
2026-09-02 00:42:36,160 | INFO | __main__ | Archivo recibido como parámetro: /Users/tamita/development/pragma/prueba-data-engineer/data/raw/2012-1.csv
2026-09-02 00:42:36,160 | INFO | __main__ | Inicio del pipeline
2026-09-02 00:42:36,160 | INFO | src.load.db_bootstrap | Verificando si la base de datos PostgreSQL 'prueba_data_engineer' existe
2026-09-02 00:42:36,182 | INFO | src.load.db_bootstrap | La base de datos 'prueba_data_engineer' ya existe
2026-09-02 00:42:36,182 | INFO | src.extract.data_extractor | Iniciando lectura del CSV desde /Users/tamita/development/pragma/prueba-data-engineer/data/raw/2012-1.csv
2026-09-02 00:42:36,188 | INFO | src.extract.data_extractor | CSV cargado exitosamente con 22 filas y 3 columnas
2026-09-02 00:42:36,188 | INFO | src.transform.data_transformer | Iniciando pipeline de transformación del DataFrame
2026-09-02 00:42:36,188 | INFO | src.transform.data_transformer | Agregando columna source_file con valor: 2012-1.csv
2026-09-02 00:42:36,189 | INFO | src.transform.data_transformer | Columna source_file agregada. Forma del DataFrame: (22, 4)
2026-09-02 00:42:36,189 | INFO | src.transform.data_transformer | Iniciando conversión de timestamp a datetime
2026-09-02 00:42:36,192 | INFO | src.transform.data_transformer | Conversión de timestamp completada. Dtype: datetime64[us]
2026-09-02 00:42:36,192 | INFO | src.transform.data_transformer | Pipeline de transformación completado. Forma final: (22, 4), columnas: ['timestamp', 'price', 'user_id', 'source_file']
2026-09-02 00:42:36,192 | INFO | src.transform.data_transformer | Generando estadísticas acumulables del DataFrame
2026-09-02 00:42:36,193 | INFO | src.transform.data_transformer | Estadísticas generadas: total_rows=22, price_sum=1193.0, price_min=14.0, price_max=97.0
2026-09-02 00:42:36,193 | INFO | src.load.data_loader | Iniciando carga a PostgreSQL para la tabla 'public.transactions'
2026-09-02 00:42:36,193 | INFO | src.load.db_connector | Creando engine de PostgreSQL para la base de datos 'prueba_data_engineer'
2026-09-02 00:42:36,205 | INFO | src.load.db_connector | Engine de PostgreSQL creado exitosamente
2026-09-02 00:42:36,234 | INFO | src.load.data_loader | Carga a PostgreSQL completada exitosamente para la tabla 'public.transactions'
2026-09-02 00:42:36,234 | INFO | src.load.data_loader | Actualizando acumuladores de estadísticas en PostgreSQL
2026-09-02 00:42:36,234 | INFO | src.load.db_connector | Creando engine de PostgreSQL para la base de datos 'prueba_data_engineer'
2026-09-02 00:42:36,234 | INFO | src.load.db_connector | Engine de PostgreSQL creado exitosamente
2026-09-02 00:42:36,249 | INFO | src.load.data_loader | Acumuladores actualizados/insertados en 'public.pipeline_stats'
2026-09-02 00:42:36,249 | INFO | __main__ | Pipeline se ejecutó exitosamente
2026-09-02 00:42:36,293 - __main__ - INFO -
2026-09-02 00:42:36,293 - __main__ - INFO - Ejecutando pipeline para: /Users/tamita/development/pragma/prueba-data-engineer/data/raw/2012-2.csv
2026-09-02 00:42:36,293 - __main__ - INFO -
2026-09-02 00:42:36,552 | INFO | __main__ | Archivo recibido como parámetro: /Users/tamita/development/pragma/prueba-data-engineer/data/raw/2012-2.csv
2026-09-02 00:42:36,552 | INFO | __main__ | Inicio del pipeline
2026-09-02 00:42:36,552 | INFO | src.load.db_bootstrap | Verificando si la base de datos PostgreSQL 'prueba_data_engineer' existe
2026-09-02 00:42:36,572 | INFO | src.load.db_bootstrap | La base de datos 'prueba_data_engineer' ya existe
2026-09-02 00:42:36,572 | INFO | src.extract.data_extractor | Iniciando lectura del CSV desde /Users/tamita/development/pragma/prueba-data-engineer/data/raw/2012-2.csv
2026-09-02 00:42:36,574 | INFO | src.extract.data_extractor | CSV cargado exitosamente con 29 filas y 3 columnas
2026-09-02 00:42:36,574 | INFO | src.transform.data_transformer | Iniciando pipeline de transformación del DataFrame
2026-09-02 00:42:36,574 | INFO | src.transform.data_transformer | Agregando columna source_file con valor: 2012-2.csv
2026-09-02 00:42:36,574 | INFO | src.transform.data_transformer | Columna source_file agregada. Forma del DataFrame: (29, 4)
2026-09-02 00:42:36,574 | INFO | src.transform.data_transformer | Iniciando conversión de timestamp a datetime
2026-09-02 00:42:36,575 | INFO | src.transform.data_transformer | Conversión de timestamp completada. Dtype: datetime64[us]
2026-09-02 00:42:36,575 | INFO | src.transform.data_transformer | Pipeline de transformación completado. Forma final: (29, 4), columnas: ['timestamp', 'price', 'user_id', 'source_file']
2026-09-02 00:42:36,575 | INFO | src.transform.data_transformer | Generando estadísticas acumulables del DataFrame
2026-09-02 00:42:36,576 | INFO | src.transform.data_transformer | Estadísticas generadas: total_rows=29, price_sum=1590, price_min=10, price_max=100
2026-09-02 00:42:36,576 | INFO | src.load.data_loader | Iniciando carga a PostgreSQL para la tabla 'public.transactions'
2026-09-02 00:42:36,576 | INFO | src.load.db_connector | Creando engine de PostgreSQL para la base de datos 'prueba_data_engineer'
2026-09-02 00:42:36,586 | INFO | src.load.db_connector | Engine de PostgreSQL creado exitosamente
2026-09-02 00:42:36,604 | INFO | src.load.data_loader | Carga a PostgreSQL completada exitosamente para la tabla 'public.transactions'
2026-09-02 00:42:36,604 | INFO | src.load.data_loader | Actualizando acumuladores de estadísticas en PostgreSQL
2026-09-02 00:42:36,604 | INFO | src.load.db_connector | Creando engine de PostgreSQL para la base de datos 'prueba_data_engineer'
2026-09-02 00:42:36,604 | INFO | src.load.db_connector | Engine de PostgreSQL creado exitosamente
2026-09-02 00:42:36,616 | INFO | src.load.data_loader | Acumuladores actualizados/insertados en 'public.pipeline_stats'
2026-09-02 00:42:36,616 | INFO | __main__ | Pipeline se ejecutó exitosamente
2026-09-02 00:42:36,656 - __main__ - INFO -
2026-09-02 00:42:36,656 - __main__ - INFO - Ejecutando pipeline para: /Users/tamita/development/pragma/prueba-data-engineer/data/raw/2012-3.csv
2026-09-02 00:42:36,656 - __main__ - INFO -
2026-09-02 00:42:36,982 | INFO | __main__ | Archivo recibido como parámetro: /Users/tamita/development/pragma/prueba-data-engineer/data/raw/2012-3.csv
2026-09-02 00:42:36,982 | INFO | __main__ | Inicio del pipeline
2026-09-02 00:42:36,982 | INFO | src.load.db_bootstrap | Verificando si la base de datos PostgreSQL 'prueba_data_engineer' existe
2026-09-02 00:42:37,018 | INFO | src.load.db_bootstrap | La base de datos 'prueba_data_engineer' ya existe
2026-09-02 00:42:37,019 | INFO | src.extract.data_extractor | Iniciando lectura del CSV desde /Users/tamita/development/pragma/prueba-data-engineer/data/raw/2012-3.csv
2026-09-02 00:42:37,020 | INFO | src.extract.data_extractor | CSV cargado exitosamente con 31 filas y 3 columnas
2026-09-02 00:42:37,020 | INFO | src.transform.data_transformer | Iniciando pipeline de transformación del DataFrame
2026-09-02 00:42:37,020 | INFO | src.transform.data_transformer | Agregando columna source_file con valor: 2012-3.csv
2026-09-02 00:42:37,021 | INFO | src.transform.data_transformer | Columna source_file agregada. Forma del DataFrame: (31, 4)
2026-09-02 00:42:37,021 | INFO | src.transform.data_transformer | Iniciando conversión de timestamp a datetime
2026-09-02 00:42:37,022 | INFO | src.transform.data_transformer | Conversión de timestamp completada. Dtype: datetime64[us]
2026-09-02 00:42:37,022 | INFO | src.transform.data_transformer | Pipeline de transformación completado. Forma final: (31, 4), columnas: ['timestamp', 'price', 'user_id', 'source_file']
2026-09-02 00:42:37,023 | INFO | src.transform.data_transformer | Generando estadísticas acumulables del DataFrame
2026-09-02 00:42:37,023 | INFO | src.transform.data_transformer | Estadísticas generadas: total_rows=31, price_sum=1850, price_min=12, price_max=99
2026-09-02 00:42:37,023 | INFO | src.load.data_loader | Iniciando carga a PostgreSQL para la tabla 'public.transactions'
2026-09-02 00:42:37,023 | INFO | src.load.db_connector | Creando engine de PostgreSQL para la base de datos 'prueba_data_engineer'
2026-09-02 00:42:37,044 | INFO | src.load.db_connector | Engine de PostgreSQL creado exitosamente
2026-09-02 00:42:37,062 | INFO | src.load.data_loader | Carga a PostgreSQL completada exitosamente para la tabla 'public.transactions'
2026-09-02 00:42:37,062 | INFO | src.load.data_loader | Actualizando acumuladores de estadísticas en PostgreSQL
2026-09-02 00:42:37,062 | INFO | src.load.db_connector | Creando engine de PostgreSQL para la base de datos 'prueba_data_engineer'
2026-09-02 00:42:37,062 | INFO | src.load.db_connector | Engine de PostgreSQL creado exitosamente
2026-09-02 00:42:37,074 | INFO | src.load.data_loader | Acumuladores actualizados/insertados en 'public.pipeline_stats'
2026-09-02 00:42:37,074 | INFO | __main__ | Pipeline se ejecutó exitosamente
2026-09-02 00:42:37,125 - __main__ - INFO -
2026-09-02 00:42:37,125 - __main__ - INFO - Ejecutando pipeline para: /Users/tamita/development/pragma/prueba-data-engineer/data/raw/2012-4.csv
2026-09-02 00:42:37,125 - __main__ - INFO -
2026-09-02 00:42:37,403 | INFO | __main__ | Archivo recibido como parámetro: /Users/tamita/development/pragma/prueba-data-engineer/data/raw/2012-4.csv
2026-09-02 00:42:37,403 | INFO | __main__ | Inicio del pipeline
2026-09-02 00:42:37,403 | INFO | src.load.db_bootstrap | Verificando si la base de datos PostgreSQL 'prueba_data_engineer' existe
2026-09-02 00:42:37,428 | INFO | src.load.db_bootstrap | La base de datos 'prueba_data_engineer' ya existe
2026-09-02 00:42:37,428 | INFO | src.extract.data_extractor | Iniciando lectura del CSV desde /Users/tamita/development/pragma/prueba-data-engineer/data/raw/2012-4.csv
2026-09-02 00:42:37,430 | INFO | src.extract.data_extractor | CSV cargado exitosamente con 30 filas y 3 columnas
2026-09-02 00:42:37,430 | INFO | src.transform.data_transformer | Iniciando pipeline de transformación del DataFrame
2026-09-02 00:42:37,430 | INFO | src.transform.data_transformer | Agregando columna source_file con valor: 2012-4.csv
2026-09-02 00:42:37,430 | INFO | src.transform.data_transformer | Columna source_file agregada. Forma del DataFrame: (30, 4)
2026-09-02 00:42:37,430 | INFO | src.transform.data_transformer | Iniciando conversión de timestamp a datetime
2026-09-02 00:42:37,431 | INFO | src.transform.data_transformer | Conversión de timestamp completada. Dtype: datetime64[us]
2026-09-02 00:42:37,431 | INFO | src.transform.data_transformer | Pipeline de transformación completado. Forma final: (30, 4), columnas: ['timestamp', 'price', 'user_id', 'source_file']
2026-09-02 00:42:37,431 | INFO | src.transform.data_transformer | Generando estadísticas acumulables del DataFrame
2026-09-02 00:42:37,432 | INFO | src.transform.data_transformer | Estadísticas generadas: total_rows=30, price_sum=1607.0, price_min=10.0, price_max=97.0
2026-09-02 00:42:37,432 | INFO | src.load.data_loader | Iniciando carga a PostgreSQL para la tabla 'public.transactions'
2026-09-02 00:42:37,432 | INFO | src.load.db_connector | Creando engine de PostgreSQL para la base de datos 'prueba_data_engineer'
2026-09-02 00:42:37,443 | INFO | src.load.db_connector | Engine de PostgreSQL creado exitosamente
2026-09-02 00:42:37,464 | INFO | src.load.data_loader | Carga a PostgreSQL completada exitosamente para la tabla 'public.transactions'
2026-09-02 00:42:37,464 | INFO | src.load.data_loader | Actualizando acumuladores de estadísticas en PostgreSQL
2026-09-02 00:42:37,464 | INFO | src.load.db_connector | Creando engine de PostgreSQL para la base de datos 'prueba_data_engineer'
2026-09-02 00:42:37,464 | INFO | src.load.db_connector | Engine de PostgreSQL creado exitosamente
2026-09-02 00:42:37,475 | INFO | src.load.data_loader | Acumuladores actualizados/insertados en 'public.pipeline_stats'
2026-09-02 00:42:37,475 | INFO | __main__ | Pipeline se ejecutó exitosamente
2026-09-02 00:42:37,516 - __main__ - INFO -
2026-09-02 00:42:37,517 - __main__ - INFO - Ejecutando pipeline para: /Users/tamita/development/pragma/prueba-data-engineer/data/raw/2012-5.csv
2026-09-02 00:42:37,517 - __main__ - INFO -
2026-09-02 00:42:37,879 | INFO | __main__ | Archivo recibido como parámetro: /Users/tamita/development/pragma/prueba-data-engineer/data/raw/2012-5.csv
2026-09-02 00:42:37,879 | INFO | __main__ | Inicio del pipeline
2026-09-02 00:42:37,879 | INFO | src.load.db_bootstrap | Verificando si la base de datos PostgreSQL 'prueba_data_engineer' existe
2026-09-02 00:42:37,901 | INFO | src.load.db_bootstrap | La base de datos 'prueba_data_engineer' ya existe
2026-09-02 00:42:37,901 | INFO | src.extract.data_extractor | Iniciando lectura del CSV desde /Users/tamita/development/pragma/prueba-data-engineer/data/raw/2012-5.csv
2026-09-02 00:42:37,902 | INFO | src.extract.data_extractor | CSV cargado exitosamente con 31 filas y 3 columnas
2026-09-02 00:42:37,902 | INFO | src.transform.data_transformer | Iniciando pipeline de transformación del DataFrame
2026-09-02 00:42:37,902 | INFO | src.transform.data_transformer | Agregando columna source_file con valor: 2012-5.csv
2026-09-02 00:42:37,903 | INFO | src.transform.data_transformer | Columna source_file agregada. Forma del DataFrame: (31, 4)
2026-09-02 00:42:37,905 | INFO | src.transform.data_transformer | Iniciando conversión de timestamp a datetime
2026-09-02 00:42:37,906 | INFO | src.transform.data_transformer | Conversión de timestamp completada. Dtype: datetime64[us]
2026-09-02 00:42:37,906 | INFO | src.transform.data_transformer | Pipeline de transformación completado. Forma final: (31, 4), columnas: ['timestamp', 'price', 'user_id', 'source_file']
2026-09-02 00:42:37,906 | INFO | src.transform.data_transformer | Generando estadísticas acumulables del DataFrame
2026-09-02 00:42:37,906 | INFO | src.transform.data_transformer | Estadísticas generadas: total_rows=31, price_sum=1806, price_min=13, price_max=100
2026-09-02 00:42:37,906 | INFO | src.load.data_loader | Iniciando carga a PostgreSQL para la tabla 'public.transactions'
2026-09-02 00:42:37,906 | INFO | src.load.db_connector | Creando engine de PostgreSQL para la base de datos 'prueba_data_engineer'
2026-09-02 00:42:37,922 | INFO | src.load.db_connector | Engine de PostgreSQL creado exitosamente
2026-09-02 00:42:37,947 | INFO | src.load.data_loader | Carga a PostgreSQL completada exitosamente para la tabla 'public.transactions'
2026-09-02 00:42:37,947 | INFO | src.load.data_loader | Actualizando acumuladores de estadísticas en PostgreSQL
2026-09-02 00:42:37,947 | INFO | src.load.db_connector | Creando engine de PostgreSQL para la base de datos 'prueba_data_engineer'
2026-09-02 00:42:37,947 | INFO | src.load.db_connector | Engine de PostgreSQL creado exitosamente
2026-09-02 00:42:37,960 | INFO | src.load.data_loader | Acumuladores actualizados/insertados en 'public.pipeline_stats'
2026-09-02 00:42:37,960 | INFO | __main__ | Pipeline se ejecutó exitosamente
2026-09-02 00:42:38,025 - __main__ - INFO -
2026-09-02 00:42:38,025 - __main__ - INFO - 3. Estadísticas de pipeline_stats después de cargar datos:
2026-09-02 00:42:38,025 - __main__ - INFO - ==================================================
2026-09-02 00:42:38,025 - __main__ - INFO - Estadísticas de pipeline_stats:
2026-09-02 00:42:38,025 - __main__ - INFO - ==================================================
2026-09-02 00:42:38,029 - __main__ - INFO - total_rows: 143
2026-09-02 00:42:38,029 - __main__ - INFO - price_sum: 8046
2026-09-02 00:42:38,029 - __main__ - INFO - price_min: 10
2026-09-02 00:42:38,029 - __main__ - INFO - price_max: 100
2026-09-02 00:42:38,029 - __main__ - INFO - price_avg: 56.27
2026-09-02 00:42:38,029 - __main__ - INFO -
2026-09-02 00:42:38,029 - __main__ - INFO - 4. Ejecutando pipeline para archivo de validación:
2026-09-02 00:42:38,029 - __main__ - INFO -
2026-09-02 00:42:38,029 - __main__ - INFO - Ejecutando pipeline para: /Users/tamita/development/pragma/prueba-data-engineer/data/raw/validation.csv
2026-09-02 00:42:38,029 - __main__ - INFO -
2026-09-02 00:42:38,379 | INFO | __main__ | Archivo recibido como parámetro: /Users/tamita/development/pragma/prueba-data-engineer/data/raw/validation.csv
2026-09-02 00:42:38,379 | INFO | __main__ | Inicio del pipeline
2026-09-02 00:42:38,379 | INFO | src.load.db_bootstrap | Verificando si la base de datos PostgreSQL 'prueba_data_engineer' existe
2026-09-02 00:42:38,399 | INFO | src.load.db_bootstrap | La base de datos 'prueba_data_engineer' ya existe
2026-09-02 00:42:38,399 | INFO | src.extract.data_extractor | Iniciando lectura del CSV desde /Users/tamita/development/pragma/prueba-data-engineer/data/raw/validation.csv
2026-09-02 00:42:38,401 | INFO | src.extract.data_extractor | CSV cargado exitosamente con 8 filas y 3 columnas
2026-09-02 00:42:38,401 | INFO | src.transform.data_transformer | Iniciando pipeline de transformación del DataFrame
2026-09-02 00:42:38,401 | INFO | src.transform.data_transformer | Agregando columna source_file con valor: validation.csv
2026-09-02 00:42:38,401 | INFO | src.transform.data_transformer | Columna source_file agregada. Forma del DataFrame: (8, 4)
2026-09-02 00:42:38,401 | INFO | src.transform.data_transformer | Iniciando conversión de timestamp a datetime
2026-09-02 00:42:38,402 | INFO | src.transform.data_transformer | Conversión de timestamp completada. Dtype: datetime64[us]
2026-09-02 00:42:38,402 | INFO | src.transform.data_transformer | Pipeline de transformación completado. Forma final: (8, 4), columnas: ['timestamp', 'price', 'user_id', 'source_file']
2026-09-02 00:42:38,403 | INFO | src.transform.data_transformer | Generando estadísticas acumulables del DataFrame
2026-09-02 00:42:38,403 | INFO | src.transform.data_transformer | Estadísticas generadas: total_rows=8, price_sum=334, price_min=11, price_max=92
2026-09-02 00:42:38,403 | INFO | src.load.data_loader | Iniciando carga a PostgreSQL para la tabla 'public.transactions'
2026-09-02 00:42:38,403 | INFO | src.load.db_connector | Creando engine de PostgreSQL para la base de datos 'prueba_data_engineer'
2026-09-02 00:42:38,416 | INFO | src.load.db_connector | Engine de PostgreSQL creado exitosamente
2026-09-02 00:42:38,433 | INFO | src.load.data_loader | Carga a PostgreSQL completada exitosamente para la tabla 'public.transactions'
2026-09-02 00:42:38,433 | INFO | src.load.data_loader | Actualizando acumuladores de estadísticas en PostgreSQL
2026-09-02 00:42:38,433 | INFO | src.load.db_connector | Creando engine de PostgreSQL para la base de datos 'prueba_data_engineer'
2026-09-02 00:42:38,434 | INFO | src.load.db_connector | Engine de PostgreSQL creado exitosamente
2026-09-02 00:42:38,442 | INFO | src.load.data_loader | Acumuladores actualizados/insertados en 'public.pipeline_stats'
2026-09-02 00:42:38,442 | INFO | __main__ | Pipeline se ejecutó exitosamente
2026-09-02 00:42:38,503 - __main__ - INFO -
2026-09-02 00:42:38,504 - __main__ - INFO - 5. Estadísticas finales de pipeline_stats:
2026-09-02 00:42:38,504 - __main__ - INFO - ==================================================
2026-09-02 00:42:38,504 - __main__ - INFO - Estadísticas de pipeline_stats:
2026-09-02 00:42:38,504 - __main__ - INFO - ==================================================
2026-09-02 00:42:38,505 - __main__ - INFO - total_rows: 151
2026-09-02 00:42:38,505 - __main__ - INFO - price_sum: 8380
2026-09-02 00:42:38,505 - __main__ - INFO - price_min: 10
2026-09-02 00:42:38,505 - __main__ - INFO - price_max: 100
2026-09-02 00:42:38,505 - __main__ - INFO - price_avg: 55.50
2026-09-02 00:42:38,505 - __main__ - INFO -
2026-09-02 00:42:38,505 - __main__ - INFO - 6. Estadísticas de transactions:
2026-09-02 00:42:38,505 - __main__ - INFO - ==================================================
2026-09-02 00:42:38,505 - __main__ - INFO - Estadísticas de transactions:
2026-09-02 00:42:38,505 - __main__ - INFO - ==================================================
2026-09-02 00:42:38,506 - __main__ - INFO - total: 151
2026-09-02 00:42:38,506 - __main__ - INFO - sum_price: 8380.0
2026-09-02 00:42:38,506 - __main__ - INFO - min_price: 10.0
2026-09-02 00:42:38,506 - __main__ - INFO - max_price: 100.0
2026-09-02 00:42:38,506 - __main__ - INFO - average_price: 57.01
2026-09-02 00:42:38,506 - __main__ - INFO -
2026-09-02 00:42:38,506 - __main__ - INFO - ==================================================
2026-09-02 00:42:38,506 - __main__ - INFO - Pipeline completo finalizado
2026-09-02 00:42:38,506 - __main__ - INFO - ==================================================
```
