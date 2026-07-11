import requests
import csv

url = "https://clinicaltrials.gov/api/v2/studies"

params = {
   "query.intr": "antibody-drug conjugate",
    "query.cond": "cancer OR neoplasm OR tumor OR carcinoma",
    "pageSize": 100,
    "countTotal": "true"
}

all_studies = []
next_page_token = None

while True:
    if next_page_token:
        params["pageToken"] = next_page_token

    response = requests.get(url, params=params)
    data = response.json()

    studies = data.get("studies", [])
    all_studies.extend(studies)

    next_page_token = data.get("nextPageToken")
    print(f"Fetched {len(all_studies)} studies so far...")

    if not next_page_token:
        break

print(f"\nTotal studies fetched: {len(all_studies)}")

# Now extract the fields we care about
rows = []

for study in all_studies:
    protocol = study.get("protocolSection", {})

    identification = protocol.get("identificationModule", {})
    status = protocol.get("statusModule", {})
    sponsor = protocol.get("sponsorCollaboratorsModule", {})
    conditions = protocol.get("conditionsModule", {})
    design = protocol.get("designModule", {})
    interventions = protocol.get("armsInterventionsModule", {})

    row = {
        "nct_id": identification.get("nctId"),
        "title": identification.get("briefTitle"),
        "status": status.get("overallStatus"),
        "start_date": status.get("startDateStruct", {}).get("date"),
        "completion_date": status.get("completionDateStruct", {}).get("date"),
        "lead_sponsor": sponsor.get("leadSponsor", {}).get("name"),
        "sponsor_class": sponsor.get("leadSponsor", {}).get("class"),
        "conditions": "; ".join(conditions.get("conditions", [])),
        "phase": "; ".join(design.get("phases", [])),
        "enrollment": design.get("enrollmentInfo", {}).get("count"),
        "intervention_names": "; ".join([i.get("name", "") for i in interventions.get("interventions", [])]),
        "intervention_descriptions": " | ".join([i.get("description", "") for i in interventions.get("interventions", [])])
    }
    rows.append(row)
# Save to CSV
with open("adc_trials.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print("\nSaved to adc_trials.csv")
