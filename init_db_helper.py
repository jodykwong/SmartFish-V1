import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load env
load_dotenv()

db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")
db_user = os.getenv("DB_USER", "postgres")
db_password = os.getenv("DB_PASSWORD", "")
db_name = os.getenv("DB_NAME", "betta_fish")
db_dialect = os.getenv("DB_DIALECT", "postgresql")

print(f"DEBUG: Dialect={db_dialect}, Host={db_host}, User={db_user}, DB={db_name}")

if db_dialect == 'postgresql':
    # Connect to 'postgres' database to create the new DB
    url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/postgres"
    driver = 'postgresql'
elif db_dialect == 'mysql':
    url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/"
    driver = 'mysql'
else:
    print(f"Unknown dialect: {db_dialect}")
    sys.exit(1)

try:
    engine = create_engine(url, isolation_level="AUTOCOMMIT")
    with engine.connect() as conn:
        # Check if db exists
        if driver == 'postgresql':
            check_sql = text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
            exists = conn.execute(check_sql).fetchone()
            if not exists:
                print(f"Database {db_name} does not exist. Creating...")
                conn.execute(text(f'CREATE DATABASE "{db_name}"'))
                print("Database created successfully.")
            else:
                print(f"Database {db_name} already exists.")
        elif driver == 'mysql':
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
            print(f"Database {db_name} ensured.")
except Exception as e:
    print(f"Error initializing database: {e}")
    sys.exit(1)
