import os
from sqlalchemy import create_engine


USE_POSTGRES = False

if USE_POSTGRES:
    # grab the data from env
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "job_market_db")
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.normpath(os.path.join(base_dir, "..", "data", "job_market.db"))
    DB_URL = f"sqlite:///{db_path}"

def get_engine():
    return create_engine(DB_URL)