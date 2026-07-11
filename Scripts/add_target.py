import pandas as pd
import re

df = pd.read_csv("adc_trials_clean.csv")

# Canonical target name -> list of text variants to search for
target_map = {
    "HER2": ["her2", "her-2"],
    "TROP2": ["trop2", "trop-2"],
    "CD30": ["cd30"],
    "CD79b": ["cd79b"],
    "BCMA": ["bcma"],
    "Claudin18.2": ["claudin18.2", "claudin 18.2"],
    "Nectin-4": ["nectin-4", "nectin4"],
    "Folate Receptor": ["folate receptor", "fr-alpha", "fralpha"],
    "c-Met": ["c-met", "cmet"],
    "B7-H3": ["b7-h3", "b7h3"],
    "CD19": ["cd19"],
    "CD20": ["cd20"],
    "CD22": ["cd22"],
    "CD33": ["cd33"],
    "CD70": ["cd70"],
    "EGFR": ["egfr"],
    "PSMA": ["psma"],
    "Mesothelin": ["mesothelin"],
    "DLL3": ["dll3"],
    "ROR1": ["ror1"],
    "CEACAM5": ["ceacam5"],
    "Tissue Factor": ["tissue factor"],
    "GPRC5D": ["gprc5d"]
}

def find_target(row):
    combined_text = " ".join([
        str(row.get("title", "")),
        str(row.get("conditions", "")),
        str(row.get("intervention_descriptions", ""))
    ]).lower()

    found = []
    for canonical_name, variants in target_map.items():
        if any(variant in combined_text for variant in variants):
            found.append(canonical_name)

    if found:
        return "; ".join(sorted(set(found)))
    return "Unknown/Not Specified"

df["target_antigen"] = df.apply(find_target, axis=1)

print(df["target_antigen"].value_counts().head(20))

df.to_csv("adc_trials_final.csv", index=False)
print(f"\nSaved {len(df)} rows to adc_trials_final.csv")
