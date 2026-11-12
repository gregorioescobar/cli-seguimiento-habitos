# PLAN: CLI de seguimiento de hábitos

## Objetivo
Crear una herramienta de línea de comandos ligera para registrar hábitos diarios y consultar rachas, con persistencia local en SQLite.

## Stack elegido (ligero)
- Python 3 (stdlib)
- SQLite3 (stdlib)
- `argparse` para la CLI
- `unittest` para pruebas automatizadas

Sin dependencias externas.

## Tareas
1. [x] Scaffold del proyecto (estructura, git, README, PLAN).
2. [x] Implementar capa de datos (`src/storage.py`) para inicializar DB y operar hábitos/registros.
3. [x] Implementar CLI (`src/cli.py` + `habits.py`) con comandos: `add`, `log`, `list`, `streak`, `history`.
4. [x] Escribir pruebas unitarias de almacenamiento y CLI (`tests/`).
5. [x] Verificar que todas las pruebas pasen.
6. [x] Documentar uso y ejecución de tests en README.

## Criterios de aceptación
- Se puede agregar un hábito, registrar cumplimiento por fecha y listar hábitos.
- `streak` calcula la racha actual de días consecutivos hasta hoy (o hasta ayer si hoy no registrado) correctamente.
- `history` muestra registros de un hábito.
- Datos persisten en SQLite local.
- Pruebas automatizadas cubren lógica y comandos principales.
- No hay `TODO`, `FIXME` ni stubs.

## Comando exacto para correr los tests
```bash
python3 -m unittest discover -s tests -p "test*.py" -v
```
