DB_PATH="../../Remote-machines/Windows/firms-data.db"

duckdb "$DB_PATH" -f "$1"

