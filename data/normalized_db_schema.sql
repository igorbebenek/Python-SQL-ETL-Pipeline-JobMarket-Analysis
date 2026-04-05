CREATE TABLE dim_companies (id INTEGER PRIMARY KEY, name TEXT UNIQUE);;
CREATE TABLE dim_locations (id INTEGER PRIMARY KEY, city TEXT, country TEXT, UNIQUE(city, country));;
CREATE TABLE fact_offers (
            id INTEGER PRIMARY KEY,
            company_id INTEGER,
            location_id INTEGER,
            title TEXT,
            salary_avg_pln FLOAT,
            posting_date TIMESTAMP,
            seniority TEXT,
            FOREIGN KEY(company_id) REFERENCES dim_companies(id),
            FOREIGN KEY(location_id) REFERENCES dim_locations(id)
        );;
