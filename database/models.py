import os
from sqlalchemy import text, create_engine
from database.db_config import get_engine
import pandas as pd

PROD_DB_PATH = os.path.abspath("../data/job_market_final.db")

engine = get_engine()

with engine.connect() as conn:
    conn.execute(text(f"ATTACH DATABASE '{PROD_DB_PATH}' AS prod"))

    conn.execute(text("CREATE TABLE IF NOT EXISTS prod.dim_companies (id INTEGER PRIMARY KEY, name TEXT UNIQUE)"))
    conn.execute(text(
        "CREATE TABLE IF NOT EXISTS prod.dim_locations (id INTEGER PRIMARY KEY, city TEXT, country TEXT, UNIQUE(city, country))"))
    conn.execute(text("""
         CREATE TABLE IF NOT EXISTS prod.fact_offers (
             id INTEGER PRIMARY KEY,
             company_id INTEGER,
             location_id INTEGER,
             title TEXT,
             salary_avg_pln FLOAT,
             posting_date TIMESTAMP,
             seniority TEXT,
             FOREIGN KEY(company_id) REFERENCES dim_companies(id),
             FOREIGN KEY(location_id) REFERENCES dim_locations(id)
         )
     """))

    conn.execute(text("INSERT OR IGNORE INTO prod.dim_companies (name) SELECT DISTINCT company_name FROM offers"))
    conn.execute(
        text("INSERT OR IGNORE INTO prod.dim_locations (city, country) SELECT DISTINCT location, country FROM offers"))

    conn.execute(text("""
         INSERT INTO prod.fact_offers (company_id, location_id, title, salary_avg_pln, posting_date, seniority)
         SELECT c.id, l.id, o.title, o.salary_avg_pln, o.posting_date, o.IT_seniority_level
         FROM offers o
         JOIN prod.dim_companies c ON o.company_name = c.name
         JOIN prod.dim_locations l ON o.location = l.city AND o.country = l.country
     """))
    conn.commit()



export_engine = create_engine(f"sqlite:///{PROD_DB_PATH}")

with export_engine.connect() as export_conn:
    pd.read_sql("SELECT * FROM dim_companies", export_conn).to_csv("../data/db_normalized/dim_companies.csv", index=False)
    pd.read_sql("SELECT * FROM dim_locations", export_conn).to_csv("../data/db_normalized/dim_locations.csv", index=False)
    pd.read_sql("SELECT * FROM fact_offers", export_conn).to_csv("../data/db_normalized/fact_offers.csv", index=False)



#INTEGRITY TEST
with export_engine.connect() as conn_prod:
    fact_count = conn_prod.execute(text("SELECT COUNT(*) FROM fact_offers")).fetchone()[0]

with engine.connect() as conn_raw:
    raw_count = conn_raw.execute(text("SELECT COUNT(*) FROM offers")).fetchone()[0]

assert fact_count > 0, "Data Model Error: fact_offers is empty!"
assert fact_count >= raw_count * 0.8, f"Data Loss Alert! Raw: {raw_count}, Fact: {fact_count}"

print(f"Model integrity check passed: {fact_count} records normalized (out of {raw_count} raw offers).")