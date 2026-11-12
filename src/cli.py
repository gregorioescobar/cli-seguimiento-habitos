import argparse
import os
import sys
from .storage import (
    add_habit,
    get_connection,
    get_history,
    get_streak,
    init_db,
    list_habits,
    log_habit,
)


def default_db_path():
    return os.environ.get("HABITS_DB_PATH", os.path.join(os.getcwd(), "habits.db"))


def build_parser():
    parser = argparse.ArgumentParser(prog="habits", description="CLI de seguimiento de hábitos")
    parser.add_argument("--db", dest="db_path", default=default_db_path(), help="Ruta a la base de datos SQLite")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Agregar un nuevo hábito")
    p_add.add_argument("name", help="Nombre del hábito")

    p_log = sub.add_parser("log", help="Registrar cumplimiento de un hábito")
    p_log.add_argument("name", help="Nombre del hábito")
    p_log.add_argument("--date", dest="date", help="Fecha YYYY-MM-DD (por defecto hoy)")

    sub.add_parser("list", help="Listar hábitos")

    p_streak = sub.add_parser("streak", help="Mostrar racha actual de un hábito")
    p_streak.add_argument("name", help="Nombre del hábito")

    p_history = sub.add_parser("history", help="Mostrar historial de un hábito")
    p_history.add_argument("name", help="Nombre del hábito")

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    conn = get_connection(args.db_path)
    try:
        init_db(conn)
        if args.command == "add":
            add_habit(conn, args.name)
            print(f"Hábito agregado: {args.name.strip()}")
            return 0
        if args.command == "log":
            date = log_habit(conn, args.name, args.date)
            print(f"Registrado '{args.name}' en {date}")
            return 0
        if args.command == "list":
            habits = list_habits(conn)
            if not habits:
                print("No hay hábitos registrados.")
            else:
                for h in habits:
                    print(f"- {h['name']}")
            return 0
        if args.command == "streak":
            streak = get_streak(conn, args.name)
            print(f"Racha actual de '{args.name}': {streak} día(s)")
            return 0
        if args.command == "history":
            dates = get_history(conn, args.name)
            if not dates:
                print(f"Sin registros para '{args.name}'.")
            else:
                for d in dates:
                    print(d)
            return 0
        parser.print_help()
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
