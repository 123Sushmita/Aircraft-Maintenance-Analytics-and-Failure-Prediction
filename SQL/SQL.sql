CREATE DATABASE lockheed_maintenance;
USE lockheed_maintenance;


CREATE TABLE aircraft (
    aircraft_ids VARCHAR(10) PRIMARY KEY,
    aircraft_type VARCHAR(20),
    base VARCHAR(30),
    year_built INT,
    total_flight_hours INT,
    max_flight_hours INT,
    manufacturer VARCHAR(30),
    age_years INT,
    wear_score FLOAT
);

CREATE TABLE technicians (
    technician_id VARCHAR(10) PRIMARY KEY,
    department VARCHAR(30),
    certification_level VARCHAR(20),
    years_experience INT,
    base VARCHAR(30),
    active INT,
    hourly_rate_usd INT
);

CREATE TABLE maintenance_logs (
    log_id VARCHAR(10) PRIMARY KEY,
    aircraft_id VARCHAR(10),
    technician_id VARCHAR(10),
    maintenance_type VARCHAR(30),
    status VARCHAR(20),
    cost_usd FLOAT,
    duration_hours FLOAT,
    log_date DATE,
    parts_replaced INT,
    notes TEXT,
    year INT,
    quarter INT,
    failure_within_30d INT
);

# count 
SELECT COUNT(*) FROM aircraft;
SELECT COUNT(*) FROM technicians;
SELECT COUNT(*) FROM maintenance_logs;



# all failed maintenance jobs that cost more than $10,000
SELECT log_id, aircraft_id, status, cost_usd, maintenance_type
FROM maintenance_logs
WHERE status = 'failed'
AND cost_usd > 10000;

# we will get 1000 of results from here so lets try using count to get exact output

SELECT COUNT(*) as total_failed_over_10k
FROM maintenance_logs
WHERE status = 'failed'
AND cost_usd > 10000; 


 -- so, the output is 1063. 1,063 high-cost failures represent significant budget impact averaging over $10,000 each
 
 
 #  the top 5 most expensive maintenance jobs ever
 
SELECT log_id, maintenance_type, cost_usd, status
FROM maintenance_logs
ORDER BY cost_usd  desc
LIMIT  5;
 
-- All top 5 most expensive maintenance jobs are Engine Inspections
-- confirming it as the highest cost maintenance type in the fleet
 
# the total cost, average cost and count of jobs per maintenance type
SELECT maintenance_type, 
       COUNT(aircraft_id) as `no of jobs`,
       SUM(cost_usd) as total_cost,
       AVG(cost_usd) as avg_cost
FROM maintenance_logs
GROUP BY maintenance_type
ORDER BY total_cost DESC;

-- Engine Inspection accounts for over $102 million in total maintenance costs more than any other job type. 
-- Combined with Avionics Check ($62M) and Hydraulic System Repair ($69M), these three types alone represent over $234 million in maintenance spend


# Which maintenance types have an average cost above $8,000?

SELECT maintenance_type,
       AVG(cost_usd) as avg_cost
FROM maintenance_logs
GROUP BY maintenance_type
HAVING avg_cost > 8000
ORDER BY avg_cost DESC;

-- Only 3 out of 8 maintenance types exceed $8,000 average cost  Engine Inspection, Hydraulic System Repair, and Avionics Check.
 -- These should be the focus of cost optimization efforts
 
 # Show me each maintenance log with the aircraft type and base it belongs to
 SELECT ml.log_id, 
       ml.cost_usd, 
       ml.status,
       a.aircraft_type, 
       a.base
FROM maintenance_logs ml
JOIN aircraft a 
ON ml.aircraft_id= a.aircraft_ids;


#Show me each maintenance log with BOTH the aircraft type AND the technician name who did the work.
SELECT ml.log_id, 
       ml.cost_usd,
       ml.status,
       a.aircraft_type,
       t.department,
       t.certification_level
FROM maintenance_logs ml
JOIN aircraft a ON ml.aircraft_id = a.aircraft_ids
JOIN technicians t ON ml.technician_id = t.technician_id
LIMIT 10;

# Label each job as 'High Cost', 'Medium Cost' or 'Low Cost' based on cost_usd

SELECT log_id,
       cost_usd,
       CASE 
           WHEN cost_usd > 15000 THEN 'HIGH COST'
           WHEN cost_usd BETWEEN 5000 AND 15000 THEN 'MEDIUM COST'
           ELSE 'LOW COST'
       END AS cost_category
FROM maintenance_logs
LIMIT 10;

# Show all jobs that cost more than the average cost
SELECT log_id, maintenance_type, cost_usd
FROM maintenance_logs
WHERE cost_usd > (SELECT avg(cost_usd)FROM maintenance_logs)
LIMIT 10;

# Rank each maintenance job by cost within each maintenance type

SELECT log_id,
       maintenance_type,
       cost_usd,
       RANK() OVER (
           PARTITION BY maintenance_type 
           ORDER BY cost_usd DESC
       ) AS cost_rank
FROM maintenance_logs
LIMIT 20;


# Which aircraft type has the highest failure rate AND highest average cost  combined ranking?
SELECT 
    a.aircraft_type,
    COUNT(*) as total_jobs,
    ROUND(AVG(ml.cost_usd), 2) as avg_cost,
    ROUND(SUM(CASE WHEN ml.status = 'failed' 
              THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) 
              as failure_rate_pct
FROM maintenance_logs ml
JOIN aircraft a ON ml.aircraft_id = a.aircraft_ids
GROUP BY a.aircraft_type
ORDER BY failure_rate_pct DESC, avg_cost DESC;


-- C-130J has the highest failure rate at 8.57% while E-3 Sentry has the highest average maintenance cost at $7,515
-- suggesting different risk profiles requiring different management strategies
