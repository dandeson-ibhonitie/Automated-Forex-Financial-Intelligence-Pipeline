# Automated-Forex-Financial-Intelligence-Pipeline
An end-to-end Forex ETL pipeline with automated volatility risk detection. Built with Python, Requests, and Pandas, it extracts live rates, filters regional corridors, logs metrics, and appends data to an idempotent SQLite warehouse. Features strict quality gates and error handling to block duplicate entries.


# Production-Grade Forex ETL Pipeline with Automated Volatility Detection & Relational Data Warehouse Storage

##  Business Scenario (The "Why")
In international FinTech platforms, processing cross-border transactions exposes operations to extreme currency fluctuation risks. If exchange rates spike or drop suddenly and conversion layers fail to update in real-time, the platform faces thousands of dollars in transactional losses. 

This project implements a decoupled, end-to-end (E2E) ETL data pipeline. It hooks directly into live financial data nodes, extracts daily exchange rates, triggers automated volatility risk classifiers, enforces strict data quality gates, and appends logs sequentially into an idempotent data warehouse.

---

##  Architecture & Data Flow Layout

```text
[ Live Forex API ] ──► [ 1_extract.py ] ──► [ raw_rates.json ] (Audit Trail)
                                                    │
                                                    ▼
[ Volatile Alerts ] ◄── [ 2_transform.py ] ◄────────┘
            │
            ▼
     [ 3_load.py ] ──► [ forex_warehouse.db (SQLite3) ]
```

1. **Extract (`1_extract.py`)**: Streams daily mid-market currency evaluations from live servers. It saves an unedited text snapshot to establish an immutable, legal financial audit trail.
2. **Transform (`2_transform.py`)**: Ingests raw text data structures into a Pandas DataFrame. It isolates targeted regional corridors, filters broken values, and feature-engineers an operational risk classification layer.
3. **Load (`3_load.py`)**: Constructs an explicit relational database schema and executes transaction-safe appending loops guarded by strict structural database keys.

---

## 📋 Data Warehouse Schema Definition

The historical data ledger table (`exchange_logs`) enforces strict data mapping using the following configuration layout:

| Column Name | Data Type | Constraint / Rule | Purpose / Logic |
| :--- | :--- | :--- | :--- |
| **Currency** | TEXT | PRIMARY KEY (1) | Standard targeted regional transaction corridor code (`NGN`, `EUR`, `KES`, `GBP`). |
| **Rate** | REAL | NOT NULL | Cleaned transformation mid-market exchange decimal values vs USD baseline. |
| **Risk_Status** | TEXT | NOT NULL | Feature-engineered operational metric risk classifier (`HIGH RISK` / `STABLE`). |
| **Execution_Date**| TEXT | PRIMARY KEY (2) | Timeline stamp matrix extracted directly from live financial headers. |

---

## 🛠️ Pipeline Components & Implementation

### 1. Ingestion Engine (`1_extract.py`)
Connects to the open financial web node. It masks scripts with dynamic `User-Agent` browser signatures to bypass server firewalls and dumps the payload into a local backup directory.
*   **Production Feature**: Integrates defensive network validation using `response.raise_for_status()` to abort execution safely if server downtimes occur.

### 2. Volatility Detection Engine (`2_transform.py`)
Parses raw JSON streams into Pandas structures, narrowing down the scope to four essential regional markets: Nigerian Naira (`NGN`), Kenyan Shilling (`KES`), Euro (`EUR`), and British Pound (`GBP`).
*   **Production Feature**: Implements an operational quality gate to drop missing (`null`) entries or dead values (`Rate <= 0`).
*   **Production Feature**: Leverages row-wise vector functions via `.apply()` to flag currency vulnerabilities against explicit FinTech risk thresholds:
    *   *NGN >= 1500.0* | *KES >= 130.0* | *EUR >= 0.95* | *GBP >= 0.80*

### 3. Historical Tracking Architecture (`3_load.py`)
Streams clean dataframes straight into relational targets using continuous appending mechanics.
*   **Production Feature: Idempotency**. Implements a composite unique rule `PRIMARY KEY (Currency, Execution_Date)`. If the pipeline is executed multiple times on the same day, a Python `try/except sqlite3.IntegrityError` block gracefully intercepts the duplication crash, prevents data warping, and logs a clean operational warning status.

---

##  How To Run & Test Locally

### Prerequisites
Ensure your terminal environment has Python 3.x and the necessary processing libraries installed:
```bash
pip install pandas requests fake-useragent
```

### Execution Assembly Line
Run the components sequentially from your command terminal to execute the ETL pipeline:

```bash
# Step 1: Fetch raw data stream
python 1_extract.py

# Step 2: Clean and classify market risks
python 2_transform.py

# Step 3: Append records safely to database warehouse
python 3_load.py
```

### Verification & Conflict Resolution Log
If you run `python 3_load.py` multiple times on the same day, the database will block duplicate lines and activate its protective warning logging instead of throwing a system error:
```text
 Status: Duplicate data detected for this date. Ingestion skipped to protect data integrity.

..... DATA WAREHOUSE VERIFICATION LOG ......
  Currency         Rate Risk_Status                   Execution_Date
0      EUR     0.856026      Stable  Mon, 24 Aug 2026 00:02:31 +0000
1      GBP     0.732997      Stable  Mon, 24 Aug 2026 00:02:31 +0000
2      KES   129.422589      Stable  Mon, 24 Aug 2026 00:02:31 +0000
3      NGN  1340.855361      Stable  Mon, 24 Aug 2026 00:02:31 +0000

Database connection safely closed.
```
