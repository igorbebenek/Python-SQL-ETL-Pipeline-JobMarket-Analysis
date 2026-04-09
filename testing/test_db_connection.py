from database.db_config import get_engine
from sqlalchemy import text

def test_db():
    engine = get_engine()
    with engine.connect() as conn:
        res = conn.execute(text("SELECT name FROM sqlite_master WHERE name='offers'")).fetchone()
        assert res is not None, "Table offers doesn't exist!"
    print("OK")

if __name__ == "__main__":
    test_db()