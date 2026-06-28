def get_kpi_query():
    return """
        SELECT
            COUNT(*) AS total_jobs,
            COALESCE(SUM(cost_usd),0) AS total_cost,
            COALESCE(AVG(cost_usd),0) AS avg_cost,
            COALESCE(MAX(cost_usd),0) AS max_cost,
            COALESCE(MIN(cost_usd),0) AS min_cost
        FROM maintenance_logs
    """


def get_kri_query():
    return """
        SELECT
            SUM(CASE WHEN status='failed' THEN 1 ELSE 0 END) AS failed_jobs,
            SUM(CASE WHEN cost_usd > 20000 THEN 1 ELSE 0 END) AS high_risk_jobs
        FROM maintenance_logs
    """


def get_aircraft_query():
    return """
        SELECT aircraft_id, COUNT(*) AS c
        FROM maintenance_logs
        GROUP BY aircraft_id
    """


def get_maintenance_query():
    return """
        SELECT maintenance_type, COUNT(*) AS c
        FROM maintenance_logs
        GROUP BY maintenance_type
    """


def get_status_query():
    return """
        SELECT status, COUNT(*) AS c
        FROM maintenance_logs
        GROUP BY status
    """
