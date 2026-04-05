# Python SQL ETL Pipeline: Job Market Analysis

**Automated data engineering pipeline for extracting job market insights via Adzuna REST API. Focused on salary distribution and transparency and temporal posting trends.**

![Python](https://img.shields.io/badge/python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-2.0+-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/matplotlib-3.8+-00758F?style=for-the-badge&logo=matplotlib&logoColor=white)
![Seaborn](https://img.shields.io/badge/seaborn-0.13+-3776AB?style=for-the-badge&logo=seaborn&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-3.41+-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)

## Overview
A robust data engineering project that automates the complete ETL (Extract, Transform, Load) lifecycle. This pipeline extracts job market data from the Adzuna API, focusing on a robust, multi-stage processing flow to ensure data quality and integrity before analysis.

### Key Stages of the Pipeline

| Stage | Technical Description                                                                                                                                         |
| :--- |:--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Extraction** | Fetches raw data from Adzuna REST API (PL, GB, US). Handles API rate limits and missing fields. Stores raw output as JSON.                                    |
| **Transformation & EDA** | Processes JSON via Pandas. Performs deduplication, currency standardization, and null handling. Loads data into a flat SQLite table for exploratory analysis. |
| **Analysis** | Uses the flat SQLite table to perform SQL queries and generate Python visualizations (trends, distributions, and data quality checks).                        |
| **Normalization** | Migrates data from the flat table into a normalized SQL schema.                                                                                               |                                           |                                |


##  Project Structure

```text
Job_Monitor/
├── data/
│   ├── db_normalized/       # Exported CSVs for normalized schema (dim/fact)
│   ├── processed/           # Cleaned and transformed datasets
│   ├── raw/                 # Raw SQLite databases (flat tables)
│   └── normalized_db_schema.sql  # SQL DDL script for the final database schema
├── database/
│   ├── db_config.py         # SQLAlchemy engine & session setup
│   └── models.py            # SQL schema definitions (ORM models)
├── notebooks/
│   ├── 01_etl_pipeline.ipynb                # Data extraction & cleaning
│   ├── 02_salary_distribution.ipynb        # Analysis of pay ranges
│   ├── 03_day_of_the_week_influence.ipynb  # Temporal posting trends
│   └── 04_employers_by_country.ipynb       # Analysis of top employers by country
├── Testing/
│   ├── test_db_connection.py # Database integrity checks
│   └── test_ingestion.py      # API data load validation
├── .gitignore               # Files excluded from version control
├── api_client.py            # Adzuna API integration logic
├── README.md                # Project documentation and overview
└── requirements.txt         # Project dependencies

````
---

---

## Installation

### Prerequisites

* **Python 3.11** or higher
* **Git**
* **Adzuna API Credentials** (App ID & API Key)

### Step 1: Clone & Create Virtual Environment

**Windows (PowerShell)**

```powershell
# Clone the repository
git clone https://github.com/igorbebenek/Python-SQL-ETL-Pipeline-JobMarket-Analysis.git
cd Python-SQL-ETL-Pipeline-JobMarket-Analysis
# Create virtual environment
python -m venv .venv

# Activate environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```
**Linux / WSL**

```Linux/WSL
# Clone the repository
git clone https://github.com/igorbebenek/Python-SQL-ETL-Pipeline-JobMarket-Analysis.git
cd Python-SQL-ETL-Pipeline-JobMarket-Analysis

# Create virtual environment
python3 -m venv .venv

# Activate environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```
### Step 2: Environment Setup
1. Create a `.env` file in the project root with your Adzuna API credentials:

```env
APP_ID=your_app_id_here
APP_KEY=your_api_key_here
```
### Step 3: Fetch Data from Adzuna API 
````
Run api_client.py to extract job market data for Poland, Great Britain, and the United States. 
This will create raw JSON files in the `data/raw/` directory.
````
### Step 4: Run the ETL Pipeline
````
Execute the 01_etl_pipeline.ipynb notebook to perform data transformation, cleaning, and loading into the SQLite database.
````
### Step 5: Perform Analysis
````
Use the subsequent notebooks (02_salary_distribution.ipynb, 03_day_of_the_week_influence.ipynb, 04_employers_by_country.ipynb) to analyze salary distributions, temporal posting trends, and top employers by country.
````
### Step 6: Normalize Data
````
Run models.py to migrate data from the flat SQLite table into a normalized schema.
````
##  Architecture & Design Patterns

The system is designed with a focus on Data Integrity and Pipeline Resilience. It follows a modular approach to separate concerns between data retrieval, processing, and storage.

### Key Concepts:

| Concept | Implementation                                                                                                                             |
| :--- |:-------------------------------------------------------------------------------------------------------------------------------------------|
| **Data Lineage** | Raw API responses are persisted as JSON before any processing. This allows for re-running transformations without re-consuming API limits. |
| **Rate Limiting** | Built-in mechanisms to respect Adzuna API constraints, preventing 429 errors and ensuring long-running stability.                          |
| **Schema Evolution** | Transition from a flexible Flat Table (optimized for rapid EDA) to a Normalized Relational Schema (optimized for production storage).      |
| **Atomic Loading** | Ensures that data is validated and cleaned before being committed to the final SQL tables, preventing database corruption.                 |
| **Separation of Concerns** | Distinct logic layers for API Interaction (`api_client.py`), Database Logic (`models.py`), and Analytics (`notebooks/`).                   |

### Database Schema:
The final normalized database schema:

```sql
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
```

### Testing 
The `Testing/` directory contains unit tests to validate database connections and data ingestion processes. These tests ensure that the ETL pipeline functions correctly and that the database schema is properly enforced.
There are tests at the end of `01_etl_pipeline.ipynb` that validate the integrity of the data 

