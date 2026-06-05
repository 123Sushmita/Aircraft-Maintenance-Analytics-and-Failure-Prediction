# ✈️ Aircraft Maintenance Analytics & Failure Prediction
### Simulated Lockheed Martin Defense Operations Dataset

---

## 📌 Project Overview
An end-to-end data analytics project simulating a large-scale 
aircraft maintenance operation. Built to demonstrate skills in 
SQL, Python, data munging, statistics, machine learning, and 
data visualization.

---

## 📊 Dataset
| Table | Rows | Description |
|-------|------|-------------|
| aircraft | 150 | Aircraft specs, wear scores |
| technicians | 200 | Technician profiles, certifications |
| maintenance_logs | 50,000 | 4 years of maintenance records |

**Date range:** January 2021 — December 2024  
**Aircraft types:** F-35A, F-35B, F-35C, C-130J, CH-53K, UH-60M, AH-64E, F-22A, B-1B, E-3 Sentry  
**Bases:** Edwards AFB, Eglin AFB, Nellis AFB, Langley AFB, Hill AFB

---

## 🔧 Skills Demonstrated
- **Python** — numpy, pandas, matplotlib, seaborn, scikit-learn
- **Data Munging** — null handling, deduplication, type fixing, standardization
- **Statistics** — descriptive stats, correlation analysis, distribution analysis
- **Machine Learning** — Random Forest Classifier, feature importance
- **Data Visualization** — bar charts, heatmaps, trend analysis

---

## 📁 Project Structure

├── lockheed_maintenance_analytics.ipynb  ← main notebook
├── aircraft.csv                          ← aircraft table
├── technicians.csv                       ← technicians table
├── maintenance_logs.csv                  ← main fact table
└── README.md


---

## 🔍 Key Findings

### 1. Quarterly Cost Trends
> Q1 consistently shows higher average maintenance costs 
> across all years — suggesting seasonal patterns driven 
> by winter weather wear or post-holiday budget resets.

### 2. Highest & Lowest Cost Maintenance
> Engine Inspection averages $16,554 — 9.5x more expensive 
> than Software Update at $1,739.

### 3. Failure Rate by Aircraft Type
> B-1B bombers have the highest failure rate at 32.6%, 
> nearly 70% higher than E-3 Sentry at 19.1%.
> B-1B, CH-53K and F-35B require priority attention.

### 4. Base Activity
> Edwards AFB handles the most maintenance (13,385 jobs) 
> while Hill AFB has the highest failure rate at 29%.

### 5. ML Model — Failure Prediction
> Random Forest achieved 77% accuracy predicting failures.  
> Duration of job was the strongest predictor at 39.2%.

---

## 🤖 Machine Learning
| Item | Detail |
|------|--------|
| Model | Random Forest Classifier |
| Trees | 100 |
| Accuracy | 77.31% |
| Top Feature | duration_hours (39.2%) |
| Problem Type | Binary Classification |

---

## 🚀 How to Run
1. Clone this repository
2. Open `lockheed_maintenance_analytics.ipynb` in Google Colab
3. Run all cells in order

---

## 👤 About
Built as a portfolio project targeting a Data Analyst Associate 
role at Lockheed Martin. Covers every technical requirement 
in the job description:
✅ Python scripting
✅ Data munging  
✅ Descriptive & inferential statistics
✅ AI/ML experience
✅ Data visualization



