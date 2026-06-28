import os
import re

from flask import Flask, render_template, request, jsonify
import mysql.connector

from query_map import (
    get_kpi_query,
    get_kri_query,
    get_aircraft_query,
    get_maintenance_query,
    get_status_query,
)

app = Flask(__name__)  # static_folder="static", template_folder="templates" are the defaults


def db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1996",
        database="lockheed_maintenance",
        autocommit=True,
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/dashboard")
def dashboard():
    conn = db()
    cur = conn.cursor(dictionary=True)

    cur.execute(get_kpi_query())
    kpi = cur.fetchone()

    cur.execute(get_kri_query())
    kri = cur.fetchone()

    cur.execute(get_aircraft_query())
    aircraft = cur.fetchall()

    cur.execute(get_maintenance_query())
    maintenance = cur.fetchall()

    cur.execute(get_status_query())
    status = cur.fetchall()

    conn.close()

    return jsonify({
        "kpi": kpi or {},
        "kri": kri or {},
        "aircraft": aircraft or [],
        "maintenance": maintenance or [],
        "status": status or []
    })


@app.route("/api/aircraft")
def aircraft():
    conn = db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT DISTINCT aircraft_id FROM maintenance_logs")
    data = cur.fetchall()
    conn.close()
    return jsonify(data)


@app.route("/api/aircraft/<aid>")
def history(aid):
    conn = db()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT log_id, aircraft_id, maintenance_type, cost_usd, status, log_date
        FROM maintenance_logs
        WHERE aircraft_id=%s
        ORDER BY log_date DESC
    """, (aid,))

    data = cur.fetchall()
    conn.close()
    return jsonify(data)


# ---------------- CHAT (rule-based, runs real SQL, no API key needed) ----------------

AIRCRAFT_ID_PATTERN = re.compile(r"AC-?\s?(\d{3,4})", re.IGNORECASE)

DEFAULT_SUGGESTIONS = [
    "What's the total maintenance cost across the fleet?",
    "Which maintenance type costs us the most?",
    "How many jobs have failed, and is that high?",
    "Which aircraft has the most maintenance jobs?",
]


def fmt_money(n):
    try:
        return f"${float(n):,.2f}"
    except (TypeError, ValueError):
        return "$0.00"


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json or {}
    q = (data.get("q") or "").strip()
    ql = q.lower()

    if not q:
        return jsonify({
            "message": "Ask me something about the fleet — costs, failures, a specific aircraft, etc.",
            "suggestions": DEFAULT_SUGGESTIONS,
        })

    conn = db()
    cur = conn.cursor(dictionary=True)

    cur.execute(get_kpi_query())
    kpi = cur.fetchone() or {}

    cur.execute(get_kri_query())
    kri = cur.fetchone() or {}

    cur.execute(get_aircraft_query())
    jobs_per_aircraft = cur.fetchall() or []

    cur.execute(get_maintenance_query())
    maintenance_breakdown = cur.fetchall() or []

    cur.execute(get_status_query())
    status_breakdown = cur.fetchall() or []

    # If the question names a specific aircraft (e.g. "AC-0002"), pull its real history too
    mentioned_history = {}
    for match in set(AIRCRAFT_ID_PATTERN.findall(q)):
        aid = f"AC-{match.zfill(4)}"
        cur.execute("""
            SELECT log_id, maintenance_type, cost_usd, status, log_date
            FROM maintenance_logs
            WHERE aircraft_id=%s
            ORDER BY log_date DESC
            LIMIT 25
        """, (aid,))
        rows = cur.fetchall()
        if rows:
            mentioned_history[aid] = rows

    conn.close()

    message = None

    # 1) Specific aircraft mentioned -> answer from its real log
    if mentioned_history:
        parts = []
        for aid, rows in mentioned_history.items():
            total = sum(float(r["cost_usd"]) for r in rows)
            failed = sum(1 for r in rows if r["status"] == "failed")
            latest = rows[0]
            parts.append(
                f"{aid} has {len(rows)} logged job(s) totaling {fmt_money(total)}, "
                f"with {failed} marked failed. Most recent: {latest['maintenance_type']} "
                f"on {latest['log_date']} ({latest['status']})."
            )
        message = " ".join(parts)

    # 2) Which aircraft has the most jobs
    elif ("most" in ql and ("aircraft" in ql or "jobs" in ql or "maintenance" in ql)) or "highest" in ql and "aircraft" in ql:
        if jobs_per_aircraft:
            top = max(jobs_per_aircraft, key=lambda x: x["c"])
            message = f"{top['aircraft_id']} has the most maintenance jobs logged, with {top['c']} jobs."
        else:
            message = "I don't have any aircraft job data yet."

    # 3) Failure rate
    elif "fail" in ql:
        failed = kri.get("failed_jobs", 0) or 0
        total = kpi.get("total_jobs", 0) or 0
        pct = (failed / total * 100) if total else 0
        message = f"{failed} jobs have failed out of {total} total ({pct:.1f}%)."

    # 4) High risk
    elif "risk" in ql:
        hr = kri.get("high_risk_jobs", 0) or 0
        message = f"There are {hr} high-risk jobs (cost over $20,000)."

    # 5) Average cost
    elif "average" in ql or "avg" in ql:
        message = f"The average maintenance job costs {fmt_money(kpi.get('avg_cost', 0))}."

    # 6) Max cost
    elif "max" in ql or "most expensive" in ql or "highest cost" in ql:
        message = f"The most expensive single job cost {fmt_money(kpi.get('max_cost', 0))}."

    # 7) Min cost
    elif "min" in ql or "cheapest" in ql or "lowest cost" in ql:
        message = f"The cheapest single job cost {fmt_money(kpi.get('min_cost', 0))}."

    # 8) Total cost
    elif "total cost" in ql or "how much" in ql or ("total" in ql and "cost" in ql):
        message = (
            f"Total maintenance cost across the fleet is {fmt_money(kpi.get('total_cost', 0))} "
            f"across {kpi.get('total_jobs', 0)} jobs."
        )

    # 9) Maintenance type breakdown
    elif "maintenance type" in ql or any(k in ql for k in ["engine", "avionics", "hydraulic"]):
        if maintenance_breakdown:
            top = max(maintenance_breakdown, key=lambda x: x["c"])
            breakdown_str = ", ".join(f"{m['maintenance_type']}: {m['c']}" for m in maintenance_breakdown)
            message = f"Maintenance breakdown — {breakdown_str}. {top['maintenance_type']} has the most jobs."
        else:
            message = "No maintenance type data available yet."

    # 10) Status breakdown
    elif "status" in ql or "pending" in ql or "complete" in ql:
        if status_breakdown:
            breakdown_str = ", ".join(f"{s['status']}: {s['c']}" for s in status_breakdown)
            message = f"Status breakdown — {breakdown_str}."
        else:
            message = "No status data available yet."

    # 11) List aircraft
    elif "aircraft" in ql and "list" in ql:
        ids = ", ".join(a["aircraft_id"] for a in jobs_per_aircraft)
        message = f"Tracked aircraft: {ids}" if ids else "No aircraft on record yet."

    # 12) General overview
    elif any(k in ql for k in ["kpi", "kri", "summary", "overview"]):
        message = (
            f"Fleet summary — {kpi.get('total_jobs', 0)} total jobs, "
            f"{fmt_money(kpi.get('total_cost', 0))} total cost, "
            f"{fmt_money(kpi.get('avg_cost', 0))} average cost. "
            f"{kri.get('failed_jobs', 0)} failed jobs, {kri.get('high_risk_jobs', 0)} high-risk jobs."
        )

    if not message:
        message = (
            "I can answer questions about total/average/max/min cost, failure rate, "
            "high-risk jobs, maintenance types, status breakdown, or a specific aircraft "
            "(just mention its ID, e.g. AC-0002). Try one of the suggestions below."
        )

    suggestions = list(DEFAULT_SUGGESTIONS)
    if jobs_per_aircraft:
        sample_id = jobs_per_aircraft[0]["aircraft_id"]
        suggestions.append(f"How has {sample_id} been performing?")

    return jsonify({"message": message, "suggestions": suggestions})


if __name__ == "__main__":
    app.run(debug=True)
