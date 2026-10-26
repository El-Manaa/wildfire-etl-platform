DB_PATH="../../Remote-machines/Windows/firms-data.db"

function get_minio_val() {
  dotenv -f minio_c/.env.minio get "$1"
}

duckdb "$DB_PATH" <<-EOF
  LOAD httpfs;
  CREATE PERSISTENT SECRET IF NOT EXISTS minio (
    TYPE S3,
    KEY_ID '$(get_minio_val "ROOT_USER")',
    SECRET '$(get_minio_val "ROOT_PASSWORD")',
    ENDPOINT '$(get_minio_val "HOST"):$(get_minio_val "PORT")',
    USE_SSL false,
    URL_STYLE 'path'
  );
EOF
