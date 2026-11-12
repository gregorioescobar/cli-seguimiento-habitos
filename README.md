# CLI de seguimiento de hábitos

Herramienta de línea de comandos ligera para registrar hábitos diarios y consultar rachas, con persistencia local en SQLite.

## Requisitos
- Python 3.10+ (usa solo biblioteca estándar)

## Instalación / uso local
No requiere dependencias externas. Ejecuta desde el directorio del proyecto:

```bash
python3 habits.py --help
```

Por defecto la base de datos se guarda en `./habits.db` (directorio actual). Puedes cambiarla con `--db` o la variable de entorno `HABITS_DB_PATH`.

## Comandos

- Agregar hábito:
  ```bash
  python3 habits.py add "Leer"
  ```
- Registrar cumplimiento (hoy o fecha específica):
  ```bash
  python3 habits.py log "Leer"
  python3 habits.py log "Leer" --date 2026-11-12
  ```
- Listar hábitos:
  ```bash
  python3 habits.py list
  ```
- Ver racha actual:
  ```bash
  python3 habits.py streak "Leer"
  ```
  La racha cuenta días consecutivos terminando en hoy; si hoy no está registrado pero ayer sí, cuenta hasta ayer. Si se rompió la racha, devuelve 0.
- Ver historial:
  ```bash
  python3 habits.py history "Leer"
  ```

## Pruebas
Ejecuta la suite de pruebas unitarias con:

```bash
python3 -m unittest discover -s tests -p "test*.py" -v
```

## Estructura
- `habits.py`: punto de entrada CLI
- `src/storage.py`: lógica de datos (SQLite)
- `src/cli.py`: parsing de argumentos y comandos
- `tests/`: pruebas unitarias de almacenamiento y CLI
