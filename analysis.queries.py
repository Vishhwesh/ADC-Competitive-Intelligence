import pandas as pd
import sqlite3

conn = sqlite3.connect("adc_trials.db")

print("="*60)
print("Q1: Which sponsors lead the most ADC trials?")
print("="*60)
q1 = """
SELECT lead_sponsor, COUNT(*) as trial_count
FROM trials
GROUP BY lead_sponsor
ORDER BY trial_count DESC
LIMIT 10
"""
print(pd.read_sql(q1, conn))

print("\n" + "="*60)
print("Q2: How many trials by sponsor class (Industry vs Academic vs Government)?")
print("="*60)
q2 = """
SELECT sponsor_class, COUNT(*) as trial_count
FROM trials
GROUP BY sponsor_class
ORDER BY trial_count DESC
"""
print(pd.read_sql(q2, conn))

print("\n" + "="*60)
print("Q3: What's the median enrollment size by phase?")
print("="*60)
q3 = """
SELECT phase, COUNT(*) as trial_count, AVG(enrollment) as avg_enrollment
FROM trials
GROUP BY phase
ORDER BY trial_count DESC
"""
print(pd.read_sql(q3, conn))

print("\n" + "="*60)
print("Q4: Which target antigens are most studied?")
print("="*60)
q4 = """
SELECT target_antigen, COUNT(*) as trial_count
FROM trials
GROUP BY target_antigen
ORDER BY trial_count DESC
LIMIT 15
"""
print(pd.read_sql(q4, conn))

print("\n" + "="*60)
print("Q5: What's the trial status breakdown (how many terminated/withdrawn)?")
print("="*60)
q5 = """
SELECT status, COUNT(*) as trial_count,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM trials), 1) as pct_of_total
FROM trials
GROUP BY status
ORDER BY trial_count DESC
"""
print(pd.read_sql(q5, conn))

print("\n" + "="*60)
print("Q6: How has ADC trial activity trended by start year?")
print("="*60)
q6 = """
SELECT SUBSTR(start_date, 1, 4) as start_year, COUNT(*) as trial_count
FROM trials
WHERE start_date IS NOT NULL
GROUP BY start_year
ORDER BY start_year
"""
print(pd.read_sql(q6, conn))

print("\n" + "="*60)
print("Q7: Which sponsors are most active with HER2-targeted ADCs specifically?")
print("="*60)
q7 = """
SELECT lead_sponsor, COUNT(*) as her2_trial_count
FROM trials
WHERE target_antigen LIKE '%HER2%'
GROUP BY lead_sponsor
ORDER BY her2_trial_count DESC
LIMIT 10
"""
print(pd.read_sql(q7, conn))

conn.close()