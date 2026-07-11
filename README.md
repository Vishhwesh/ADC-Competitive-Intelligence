# ADC Clinical Trial Landscape — Competitive Intelligence Dashboard

A full data pipeline analyzing **540 antibody-drug conjugate (ADC) oncology clinical trials**, built from live ClinicalTrials.gov data — covering data collection, cleaning, SQL analysis, and an interactive dashboard.

**Live dashboard:** [View it here](https://vishhwesh.github.io/ADC-Competitive-Intelligence/ADC_dashboard.html)

---

## Why ADCs

Antibody-drug conjugates are one of the fastest-growing drug classes in oncology — combining a targeting antibody, a cytotoxic payload, and a linker to deliver chemotherapy directly to tumor cells while sparing healthy tissue. This project treats ADC clinical development like a competitive intelligence problem: who's building what, against which targets, and how fast is the space moving.

## What this project does

1. **Collects** real trial data directly from the ClinicalTrials.gov API (773 raw results for ADC-related search terms)
2. **Cleans and classifies** trials using a multi-layer detection method — payload/linker suffix matching (e.g. *vedotin*, *deruxtecan*, *govitecan*), explicit "antibody-drug conjugate" phrase detection, and manual verification of code-named investigational drugs — narrowing 773 raw results down to **540 confirmed ADC oncology trials**
3. **Extracts target antigens** (HER2, TROP2, CD30, Claudin18.2, and 20+ others) from trial titles, conditions, and descriptions
4. **Loads the cleaned dataset into SQLite** and answers real business questions with SQL — sponsor leadership, trial status/risk breakdown, enrollment patterns by phase, year-over-year growth
5. **Visualizes findings** in both a Power BI dashboard and a custom interactive HTML dashboard

## Key findings

- **ADC trial starts grew ~2.6× between 2018 and 2025** (30 → 79 trials/year) — this is an accelerating, not saturating, drug class
- **HER2 remains the dominant target** (~26% of trials with a known target), but Chinese biotechs (Shanghai Miracogen, RemeGen, Chia Tai Tianqing) are now rivaling Western pharma in HER2-specific trial volume
- **Seagen Inc. and the National Cancer Institute lead** by raw trial count (26 and 22 respectively)
- **~12% of trials stall** (terminated, withdrawn, or suspended) — a useful risk benchmark for this drug class
- Industry sponsors lead **58%** of trials, confirming this is a commercially-driven space, not primarily academic

## Tech stack

| Stage | Tool |
|---|---|
| Data collection | Python (`requests`), ClinicalTrials.gov API v2 |
| Cleaning & classification | Python (`pandas`), regex pattern matching |
| Analysis | SQL (SQLite via `sqlite3` / `pandas.read_sql`) |
| Visualization | Power BI Desktop, custom HTML/SVG/JS dashboard |

## Repository structure
├── fetch_data.py           # Pulls raw trial data from ClinicalTrials.gov API

├── clean_data.py           # Classifies and filters true ADC trials

├── add_target.py           # Extracts target antigen from trial text

├── load_to_sql.py          # Loads cleaned data into SQLite

├── analysis_queries.py     # Business-question SQL queries

├── explore_data.py         # Missing-value / distribution checks

├── adc_trials.csv          # Raw pulled data (773 studies)

├── adc_trials_clean.csv    # After ADC classification filter

├── adc_trials_final.csv    # Final dataset with target antigen (540 studies)

├── excluded_check.csv      # Excluded studies, for auditability

├── adc_trials.db           # SQLite database

├── ADC_dashboard.html      # Interactive dashboard (no external dependencies)

└── README.md
## Methodology notes & limitations

- A study was confirmed as an ADC trial if it matched a known payload/linker suffix, explicitly stated "antibody-drug conjugate" in its title/description, or matched a manually verified list of code-named investigational ADCs.
- **46% of confirmed trials have no identifiable target antigen** in public text — mostly early-phase, code-named compounds with minimal disclosure. This is a genuine data limitation, not a processing error, and is intentionally reported rather than hidden.
- Data reflects a snapshot pulled in July 2026 and will not include trials registered afterward.

## Author

**Vishwesh S.** — MTech Biotechnology
[LinkedIn](https://linkedin.com/in/vishwesh-s-179357200) · vishwesh348@gmail.com
