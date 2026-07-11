import pandas as pd

df = pd.read_csv("adc_trials_clean.csv")

print("Total rows:", len(df))
print("\nMissing values per column:")
print(df.isnull().sum())

print("\nEnrollment stats:")
print(df["enrollment"].describe())

print("\nUnique status values:")
print(df["status"].value_counts())

print("\nUnique sponsor_class values:")
print(df["sponsor_class"].value_counts())