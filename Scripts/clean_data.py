import pandas as pd
import re

df = pd.read_csv("adc_trials.csv")
print(f"Starting rows: {len(df)}")

adc_suffixes = [
    "vedotin", "deruxtecan", "govitecan", "emtansine", "mafodotin",
    "ozogamicin", "tesirine", "soravtansine", "duocarmazine",
    "rezetecan", "tazevibulin", "vedotinum"
]

# Manually confirmed ADC/ISAC code names found during review (no suffix, generic descriptions)
known_adc_codes = [
    "gsk2857916", "mrg002", "shr-a1403", "bnt323", "bnt324", "sgn-35",
    "db-1311", "db-1305", "bat8006", "bdc-1001", "bdc-4182", "arx788",
    "for46", "qls5133", "obi-992", "bhv-1530", "ibi3005"
]

def is_adc_by_suffix(text):
    if pd.isna(text):
        return False
    text = text.lower()
    return any(suffix in text for suffix in adc_suffixes)

def is_adc_by_phrase(text):
    if pd.isna(text):
        return False
    text = text.lower()
    if "antibody-drug conjugate" in text or "antibody drug conjugate" in text:
        return True
    if "immune-stimulating antibody conjugate" in text or "immune stimulating antibody conjugate" in text:
        return True
    # word-boundary check for standalone "ADC" (catches TR1801-ADC, RC48-ADC, etc.)
    if re.search(r'\badc\b', text):
        return True
    return False

def is_adc_by_known_code(text):
    if pd.isna(text):
        return False
    text = text.lower()
    return any(code in text for code in known_adc_codes)

df["match_suffix"] = df["intervention_names"].apply(is_adc_by_suffix)
df["match_title"] = df["title"].apply(is_adc_by_phrase)
df["match_intr_name"] = df["intervention_names"].apply(is_adc_by_phrase)
df["match_desc"] = df["intervention_descriptions"].apply(is_adc_by_phrase)
df["match_known_code"] = df["intervention_names"].apply(is_adc_by_known_code)

df["is_confirmed_adc"] = (
    df["match_suffix"] | df["match_title"] | df["match_intr_name"] |
    df["match_desc"] | df["match_known_code"]
)

print(f"Confirmed ADC trials: {df['is_confirmed_adc'].sum()}")
print(f"Excluded: {(~df['is_confirmed_adc']).sum()}")

df_clean = df[df["is_confirmed_adc"]].copy()
# Handle missing values
df_clean["phase"] = df_clean["phase"].fillna("NOT_APPLICABLE")
df_clean = df_clean.drop(columns=["match_suffix", "match_title", "match_intr_name", "match_desc", "match_known_code", "is_confirmed_adc"])
df_clean.to_csv("adc_trials_clean.csv", index=False)
print(f"\nSaved {len(df_clean)} clean rows to adc_trials_clean.csv")

df_excluded = df[~df["is_confirmed_adc"]]
df_excluded[["nct_id", "title", "intervention_names", "intervention_descriptions"]].to_csv("excluded_check.csv", index=False)
print(f"Saved {len(df_excluded)} excluded rows to excluded_check.csv for review")
