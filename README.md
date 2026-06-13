# Lockheed Martin Aircraft Maintenance Analytics and Failure Prediction

## Project Overview

This is an end-to-end data analytics project simulating a large-scale 
aircraft maintenance operation inspired by Lockheed Martin defense operations.

The core business problem this project solves:

"Can we predict which aircraft will fail within 30 days 
before it actually happens?"

The project covers the full data analytics pipeline:

- data generation, 
- data cleaning,
- exploratory analysis,
-  machine learning,
-  SQL querying,
-  business intelligence dashboards

---

## Why This Project

Real defense and aerospace data is classified and unavailable publicly.
Instead of using a generic dataset, I modeled what a realistic 
Lockheed Martin maintenance database would look like — 
with realistic cost ranges, failure rates, aircraft types, 
bases, and technician profiles.

Every column in every table exists for a specific business reason.
Every analysis answers a real question a Lockheed manager would ask.

---

## Dataset

Three tables were created to simulate a relational database:

Table: aircraft
Rows: 150
Description: Aircraft specifications, base location, 
flight hours, age, and wear score

Table: technicians
Rows: 200
Description: Technician profiles, departments, 
certification levels, and hourly rates

Table: maintenance_logs
Rows: 50,000
Description: Four years of maintenance records (2021-2024), 
the main fact table connecting aircraft and technicians

Aircraft types included:
F-35A, F-35B, F-35C, C-130J, CH-53K, 
UH-60M, AH-64E, F-22A, B-1B, E-3 Sentry

Bases included:
Edwards AFB CA, Eglin AFB FL, Nellis AFB NV, 
Langley AFB VA, Hill AFB UT

Date range: January 2021 to December 2024

---

## Project Structure

lockheed_maintenance_analytics.ipynb  - main Python notebook

aircraft.csv                          - aircraft table

technicians.csv                       - technicians table

maintenance_logs_final.csv            - cleaned maintenance logs

analysis_queries.sql                  - all 10 SQL queries

lockheed_maintenance_dashboard.pbix   - Power BI dashboard

dashboard_screenshot.png              - dashboard preview

README.md                             - project documentation

---

## Phase 1 - Data Generation

Tool: Python (numpy, pandas)

Built a realistic dataset from scratch without using any external data sources.

Key decisions made:
- Cost ranges set per maintenance type based on real-world logic.
  Engine Inspection costs between 8000 and 25000 dollars.
  Software Update costs between 500 and 3000 dollars.
  
- Status weights set to reflect real operations.
  68 percent complete, 12 percent pending, 
  12 percent in progress, 8 percent failed.
  
- Failure tendency set per aircraft type.
  B-1B has highest tendency at 22 percent.
  E-3 Sentry has lowest tendency at 9 percent.
  
- Wear score calculated per aircraft combining 
  flight hours (60 percent weight) and age (40 percent weight).
  Flight hours matter more than age for physical wear.

---

## Phase 2 - Data Munging and Cleaning

Tool: Python (pandas)

Real-world data problems were intentionally injected 
then fixed to practice data munging skills.

Problems injected and how they were fixed:

Missing values - 2500 null costs
Fix: filled with group-wise median per maintenance type.
Reason: overall median would be wrong for expensive jobs like 
Engine Inspection and cheap jobs like Software Update.

Duplicate rows - 1000 duplicates added
Fix: drop_duplicates()

Status typos - 200 inconsistent values
Examples: COMPLETE, Complete, complet
Fix: str.lower().str.strip() then replace()

Wrong data types - 1400 costs stored as dollar strings
Examples: $10,518 stored as text
Fix: removed dollar sign and comma then converted to float

Date stored as text
Fix: pd.to_datetime()

Key learning: Always fix the source of truth, 
not the downstream code.
Patching symptoms instead of root causes creates technical debt.

---

## Phase 3 - Exploratory Data Analysis and Statistics

Tool: Python (pandas, matplotlib, seaborn)

Business questions answered:

Question 1: What is the average maintenance cost per quarter?
Finding: Q1 consistently shows higher costs across all years,
suggesting seasonal patterns from winter weather wear 
or post-holiday budget resets.

Question 2: Which maintenance type costs the most and least?
Finding: Engine Inspection averages 16,557 dollars.
Software Update averages 1,739 dollars.
That is a 9.5 times difference.

Question 3: Which aircraft type fails the most?
Finding: B-1B has 32.6 percent failure rate.
E-3 Sentry has 19.1 percent failure rate.
B-1B requires priority maintenance attention.

Question 4: Which base has the most activity?
Finding: Edwards AFB handles 13,385 jobs - the most of any base.
Hill AFB has the highest failure rate at 29 percent.

Question 5: What predicts failures?
Finding: Duration hours has the strongest correlation 
with failures at 0.366.
Longer jobs are moderately linked to failures.
This guided feature selection for the ML model.

---

## Phase 4 - Machine Learning

Tool: Python (scikit-learn)

Model: Random Forest Classifier
Trees: 100
Train/Test split: 80 percent train, 20 percent test
Accuracy: 77.31 percent
Problem type: Binary classification (will it fail? yes or no)

Feature importance results:
duration_hours   - 39.2 percent - most important
cost_usd         - 31.0 percent - second
wear_score       - 18.1 percent - third
parts_replaced   - 11.6 percent - least important

Key finding: Duration of the maintenance job is the 
strongest predictor of failure. This confirms the 
correlation analysis from Phase 3.

Business impact: Instead of reacting to failures after they happen,
this model allows proactive scheduling of maintenance 
before aircraft fail. In defense operations this saves 
both cost and lives.

---

## Phase 5 - SQL Analysis

Tool: MySQL

The same cleaned dataset was loaded into MySQL 
and queried to answer business questions.

Why SQL after Python?
Python is better for cleaning, analysis, and machine learning.
SQL is better for querying large databases fast 
and answering specific business questions in production.
They are teammates, not competitors.

10 queries written:

Query 1: Failed jobs costing over 10,000 dollars
Result: 1,063 records found

Query 2: Top 5 most expensive jobs
Result: All 5 were Engine Inspections, max cost 24,998 dollars

Query 3: Total and average cost per maintenance type
Result: Engine Inspection total spend equals 102 million dollars

Query 4: Job types averaging over 8,000 dollars using HAVING
Result: Only 3 of 8 types qualify

Query 5: JOIN maintenance logs with aircraft table
Result: Added aircraft type and base to every log

Query 6: JOIN all 3 tables
Result: Combined logs, aircraft, and technician data

Query 7: CASE WHEN cost categorization
Result: Labeled every job as High, Medium, or Low cost

Query 8: Subquery - jobs above average cost
Result: Dynamic filtering without hardcoding values

Query 9: Window functions - rank jobs by cost within each type
Result: RANK() OVER PARTITION BY maintenance type

Query 10: Complex query - failure rate and avg cost by aircraft type
Result: C-130J has highest failure rate at 8.57 percent

---

## Phase 6 - Power BI Dashboard

Tool: Microsoft Power BI Desktop

Connected all three CSV files to Power BI and built 
an interactive executive dashboard.

KPI Cards:
Total jobs: 50,000
Average cost per job: 7,430 dollars
Total maintenance spend: 371 million dollars
Overall failure rate: 26 percent

Charts built:
Total jobs by base - Edwards AFB is busiest
Average cost by maintenance type - Engine Inspection highest
Failure rate by aircraft type - B-1B highest at 33 percent
Cost trend over time - line chart by month and year
Job status breakdown - donut chart
Interactive slicer - filter all visuals by base

Key feature: Clicking any base in the slicer 
updates all charts simultaneously.

---

## Key Business Insights

1. B-1B bombers have the highest failure rate at 32.6 percent,
   nearly 70 percent higher than E-3 Sentry at 19.1 percent.
   B-1B, CH-53K, and F-35B require priority maintenance attention.

2. Engine Inspection alone accounts for 102 million dollars 
   in total maintenance spend across the fleet.

3. Edwards AFB is the busiest base handling 13,385 jobs,
   while Hill AFB has the highest failure rate at 29 percent.

4. Q1 consistently shows higher maintenance costs across all years.

5. Duration of maintenance job is the strongest predictor 
   of future failures at 39.2 percent feature importance.

---

## Skills Demonstrated

Python: numpy, pandas, matplotlib, seaborn, scikit-learn
SQL: SELECT, WHERE, GROUP BY, HAVING, JOIN, 
     CASE WHEN, subqueries, window functions
Power BI: data modeling, relationships, KPI cards, 
          interactive slicers, dashboard design
Data munging: null handling, deduplication, 
              type fixing, standardization
Statistics: descriptive stats, correlation analysis, 
            distribution analysis
Machine learning: Random Forest, feature importance, 
                  train/test split, classification metrics

---

## How to Run

1. Clone this repository
2. Open lockheed_maintenance_analytics.ipynb in Google Colab
3. Run all cells in order
4. Open analysis_queries.sql in MySQL Workbench
5. Open lockheed_maintenance_dashboard.pbix in Power BI Desktop

---

## About

Built as a portfolio project targeting a Data Analyst Associate 
role at Lockheed Martin. Covers every technical requirement 
in the job description:

Python scripting - covered in Phase 1, 2, 3, 4

Data munging - covered in Phase 2

Descriptive and inferential statistics - covered in Phase 3

AI and ML experience - covered in Phase 4

Data visualization - covered in Phase 3 and Phase 6

SQL and database analysis - covered in Phase 5
