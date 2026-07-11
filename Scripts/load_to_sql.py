import pandas as pd
import sqlite3

df = pd.read_csv("adc_trials_final.csv")

conn = sqlite3.connect("adc_trials.db")
df.to_sql("trials", conn, if_exists="replace", index=False)

print("Loaded", len(df), "rows into adc_trials.db, table 'trials'")

# Quick sanity check
result = pd.read_sql("SELECT COUNT(*) as total FROM trials", conn)
print(result)

conn.close()
