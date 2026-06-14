import psycopg2
import sys

sys.stdout.reconfigure(encoding="utf-8")

conn = psycopg2.connect(
    host="localhost", port=5432, dbname="analytics_db",
    user="admin", password="tu_password_secreto"
)
cur = conn.cursor()

tables = ["project", "location", "vendor", "employee", "equipment", "cost", "schedule", "maintenance", "risk"]
for t in tables:
    cur.execute(f"SELECT COUNT(*) FROM trusted.{t}")
    cnt = cur.fetchone()[0]
    print(f"trusted.{t:15s} -> {cnt:>5} rows")

print()

cur.execute("SELECT project_id, status, budget_valid, date_valid FROM trusted.project LIMIT 5")
print("--- Project sample (status normalized, budget_valid, date_valid) ---")
for row in cur.fetchall():
    print(f"  {row}")

cur.execute(
    "SELECT cost_id, project_id, cost_variance, variance_pct, has_variance_flag "
    "FROM trusted.cost WHERE has_variance_flag = TRUE LIMIT 5"
)
print("--- Cost variance flags (|actual - planned| > 10%) ---")
for row in cur.fetchall():
    print(f"  {row}")

cur.execute(
    "SELECT schedule_id, project_id, is_behind_schedule "
    "FROM trusted.schedule WHERE is_behind_schedule = TRUE LIMIT 5"
)
print("--- Behind-schedule flags ---")
for row in cur.fetchall():
    print(f"  {row}")

cur.execute("SELECT risk_id, risk_score, prob_valid FROM trusted.risk LIMIT 5")
print("--- Risk sample (derived risk_score, prob_valid) ---")
for row in cur.fetchall():
    print(f"  {row}")

cur.close()
conn.close()
