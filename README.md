# Lockheed Martin Aircraft Maintenance Analytics and Failure Prediction

## Project Overview

This is an end-to-end **Data Analytics + Machine Learning + Full-Stack Dashboard Platform** simulating a large-scale aircraft maintenance operation inspired by Lockheed Martin defense systems.

The core business problem:

> **Can we predict which aircraft will fail within 30 days before it actually happens?**

This project evolved into a **complete data intelligence platform** covering:

- Data Engineering Pipeline
- Data Cleaning & Munging
- Exploratory Data Analysis (EDA)
- Machine Learning Model (Predictive Analytics)
- SQL Analytics Layer
- Power BI Dashboard
- Flask Web-Based Interactive Dashboard (FULL STACK ADDITION)

---

## Why This Project

Real aerospace and defense data is classified and unavailable publicly.

Instead, this project simulates a **realistic Lockheed Martin-style maintenance ecosystem** using engineered synthetic data.

Every dataset, feature, and metric is designed to reflect real-world aviation maintenance decision-making used in defense operations.

---

## Dataset Overview

Three relational tables simulate enterprise-level maintenance systems:

###  Aircraft Table (150 rows)
- Aircraft specifications
- Base location
- Flight hours
- Age
- Wear score

### Technicians Table (200 rows)
- Technician profiles
- Department
- Certification levels
- Hourly rates

###  Maintenance Logs Table (50,000 rows)
- 4 years of maintenance records (2021–2024)
- Central fact table linking aircraft + technicians

---

## Aircraft Types

F-35A, F-35B, F-35C, C-130J, CH-53K, UH-60M, AH-64E, F-22A, B-1B, E-3 Sentry

## Bases

Edwards AFB (CA), Eglin AFB (FL), Nellis AFB (NV), Langley AFB (VA), Hill AFB (UT)

---

## Project Structure
lockheed_maintenance_analytics.ipynb → EDA + ML notebook
aircraft.csv → Aircraft dataset
technicians.csv → Technician dataset
maintenance_logs_final.csv → Cleaned logs dataset
analysis_queries.sql → SQL analysis queries
lockheed_maintenance_dashboard.pbix → Power BI dashboard

lockheed-dashboard/ → Flask Web App (NEW)
│ ├── app.py
│ ├── query_map.py
│ ├── templates/
│ ├── static/
│
Lockheed Dashboard.html → Frontend export
Platform_ScreenRecorder/ → Demo video (NOT included in GitHub)

.gitignore → Clean repo configuration



---

## Phase 1 - Data Generation

Built using Python (NumPy, Pandas)

### Key Design Decisions:
- Engine Inspection: $8,000 – $25,000
- Software Update: $500 – $3,000
- Status Distribution:
  - 68% Completed
  - 12% Pending
  - 12% In Progress
  - 8% Failed

### Wear Score Formula:
- 60% Flight Hours
- 40% Aircraft Age

---

## Phase 2 - Data Cleaning

Real-world data issues were intentionally injected and fixed:

- Missing values (2,500) → Group median imputation
- Duplicates (1,000) → Removed using `drop_duplicates()`
- Status inconsistencies → Standardized strings
- Currency fields → Converted to float
- Date parsing → Standardized datetime format

### Key Insight:
> Fix data at the source, not downstream.

---

## Phase 3 - Exploratory Data Analysis

### Key Findings:

- Q1 consistently has highest maintenance cost
- Engine Inspection is ~9.5× more expensive than Software Update
- B-1B aircraft has highest failure rate (~32.6%)
- Edwards AFB is busiest base (13,385 jobs)
- Maintenance duration strongly correlates with failure (0.366)

---

## Phase 4 - Machine Learning

Model: Random Forest Classifier  
Accuracy: **77.31%**

### Feature Importance:

- duration_hours → 39.2%
- cost_usd → 31.0%
- wear_score → 18.1%
- parts_replaced → 11.6%

### Key Insight:
> Maintenance duration is the strongest predictor of aircraft failure.

### Business Impact:
Enables predictive maintenance → reduces cost, downtime, and operational risk.

---

## Phase 5 - SQL Analytics

Executed using MySQL with enterprise-level queries:

### Techniques Used:
- JOINs (multi-table relational analysis)
- CASE WHEN classification
- Subqueries
- Window functions (RANK)
- Aggregations & GROUP BY

### Key Outputs:
- Engine Inspection total cost: $102M
- 1,063 high-cost failure jobs
- C-130J shows highest failure rate (SQL analysis)
- Top 5 expensive jobs all Engine Inspections

---

## Phase 6 - Power BI Dashboard

### KPIs:
- Total Jobs: 50,000
- Total Spend: $371M
- Average Cost: $7,430
- Failure Rate: 26%

### Visuals:
- Aircraft type failure comparison
- Base-wise workload distribution
- Cost trends over time
- Maintenance type breakdown
- Interactive slicers

---

## Phase 7 - Flask Web Dashboard (FULL STACK UPGRADE)

A fully interactive analytics platform built using Flask.

### Features:
- Real-time dashboard UI
- Interactive analytics queries
- Backend data processing (`app.py`)
- Query mapping system (`query_map.py`)
- Responsive frontend (HTML/CSS/JS)

### Tech Stack:
- Flask (Backend)
- Pandas (Data processing)
- HTML/CSS/JS (Frontend)
- SQL-style query engine logic

---

## Key Business Insights

- B-1B aircraft has highest failure risk (32.6%)
- Engine Inspection dominates cost ($102M)
- Edwards AFB is highest workload base
- Hill AFB has highest failure concentration
- Maintenance duration is strongest failure predictor

---

## Skills Demonstrated

### Programming
Python (Pandas, NumPy), Flask

### Data Engineering
ETL pipelines, data cleaning, relational modeling

### Machine Learning
Random Forest, feature importance, classification modeling

### SQL
Joins, aggregations, window functions, subqueries

### Data Visualization
Power BI, Matplotlib, Seaborn

### Full Stack (NEW)
Flask + frontend dashboard development

---

## How to Run

### Clone Repository

git clone https://github.com/123Sushmita/Aircraft-Maintenance-Analytics-and-Failure-Prediction.git



cd Aircraft-Maintenance-Analytics-and-Failure-Prediction

End-to-End Flow:

Data Generation → Cleaning → Analysis → ML Model → SQL Layer → Dashboard → Web App

