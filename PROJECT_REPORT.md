# Project Report: Hospital Case Mix Index (CMI) Analytics

**Author:** Mohan
**Domain:** Data Analytics / Healthcare Analytics
**Tools Used:** Python, Pandas, NumPy, Matplotlib, Seaborn

---

## 1. Introduction

Hospitals generate large volumes of case-level data every month, covering
patient demographics, the treating doctor, and a "Case Mix Index" (CMI) value
that reflects how complex or resource-intensive a case is. Manually reviewing
this data in spreadsheets is slow and error-prone. This project builds an
automated data analytics pipeline — from raw CSV to a clean, interactive
dashboard — that lets a hospital administrator explore this data in seconds.

---

## 2. Objective

- Collect and load a hospital case-level dataset
- Clean the data: remove duplicates and handle missing values
- Perform exploratory data analysis (EDA) to uncover patterns in case volume,
  patient demographics, and doctor performance
- Present the results in a readable, well-organized way — saved charts and a
  clear text summary — so the analysis is usable by non-technical
  stakeholders

---

## 3. Dataset Description

The dataset used is `data/hospital_data.csv`, containing 10 columns:

| Column        | Type        | Description                                   |
|---------------|-------------|------------------------------------------------|
| Month         | Categorical | Month the case was recorded                     |
| Case_No       | Identifier  | Unique case ID                                  |
| DOB           | Date        | Patient date of birth                           |
| Nationality   | Categorical | Patient nationality                             |
| Gender        | Categorical | Patient gender                                  |
| DoctorLicense | Identifier  | License number of the treating doctor           |
| DoctorName    | Categorical | Name of the treating doctor                     |
| Doctor Type   | Categorical | General Physician / Specialist / Surgeon / Consultant |
| Doctor Status | Categorical | Active / Inactive / On Leave                    |
| CMI Value     | Numeric     | Case Mix Index value                            |

**Note on data source:** The CSV originally supplied for this project
contained only column headers with no actual records. To build and
demonstrate a complete, working pipeline, a synthetic dataset with the same
column structure was generated (150+ records, with intentionally injected
duplicate rows and missing values). This makes the cleaning and EDA steps
meaningful to walk through. The pipeline (`app.py`) works unchanged on any
real dataset that follows the same schema — simply replace
`data/hospital_data.csv`.

---

## 4. Methodology

### 4.1 Data Loading
The dataset is loaded using `pandas.read_csv()`. Streamlit's `@st.cache_data`
decorator is used to avoid re-reading the file on every UI interaction.

### 4.2 Data Cleaning
The following steps are applied, in order:
1. **Drop fully empty rows** — rows with no data in any column are removed.
2. **Remove duplicate records** — exact duplicate rows are dropped using
   `drop_duplicates()`.
3. **Standardize column names** — leading/trailing whitespace is stripped.
4. **Parse dates** — `DOB` is converted to a proper datetime type, and a new
   `Age` column is engineered from it.
5. **Handle missing values**
   - Categorical columns (Nationality, Gender, Doctor Type, Doctor Status,
     Month) — missing values are filled with `"Unknown"` rather than dropped,
     to avoid losing otherwise-valid case records.
   - Numeric column (`CMI Value`) — missing values are filled with the
     column median, a robust measure that resists distortion by outliers.

### 4.3 Exploratory Data Analysis
EDA was performed to answer the following questions:
- How does case volume vary by month?
- What is the distribution of CMI values across all cases?
- Does CMI value vary meaningfully by doctor type?
- What is the gender and nationality mix of patients?
- How many doctors are currently active vs. inactive vs. on leave?
- What does the age distribution of patients look like?

Visualizations were built with Matplotlib and Seaborn: bar charts, pie
charts, histograms with KDE overlays, and box plots.

### 4.4 Output & Reporting
Running `analysis.py` produces a self-contained `outputs/` folder:
- **`hospital_data_cleaned.csv`** — the cleaned dataset, ready for reuse in
  other tools (Excel, Power BI, SQL, etc.)
- **`eda_summary.txt`** — a full text summary of every statistic computed
  (cleaning steps, value counts, group averages, summary statistics)
- **`charts/`** — seven PNG charts covering case volume by month, CMI
  distribution, CMI by doctor type, gender/nationality/doctor-status
  breakdowns, and patient age distribution

This keeps the project simple and dependency-light while still producing a
readable, shareable set of results.

---

## 5. Key Findings (from the sample dataset)

- Case volume is fairly evenly spread across months, with minor peaks in
  specific months depending on the random sample generated.
- CMI values follow a right-skewed distribution, consistent with most cases
  being routine and a smaller number being more complex/resource-intensive.
- CMI value spread differs across doctor types, with Surgeons and
  Consultants generally showing wider variability than General Physicians.
- The doctor pool is split roughly evenly across Active, Inactive, and On
  Leave statuses in the sample data.

*(These findings will change once the app is pointed at a real hospital
dataset — the dashboard recalculates everything live.)*

---

## 6. Challenges & Solutions

| Challenge                                   | Solution                                                        |
|----------------------------------------------|-------------------------------------------------------------------|
| Uploaded source file had no actual data rows  | Generated a schema-matching synthetic dataset for a working demo  |
| Missing values would break numeric charts     | Imputed categorical values as "Unknown", numeric values with median |
| Duplicate case records could skew KPIs        | Removed exact duplicates before any analysis                      |
| Non-technical users need to review the results | Saved a plain-language text summary alongside labeled chart images |

---

## 7. Conclusion

This project demonstrates a complete, end-to-end data analytics workflow:
loading raw data, cleaning it responsibly, exploring it visually, and
delivering the results through an accessible web dashboard — all using core
Python data analytics tools. It is designed to be portfolio-ready and can be
directly extended to a real hospital's operational data.

---

## 8. Future Enhancements

- Connect to a live database (PostgreSQL/MySQL) instead of a static CSV
- Add predictive analytics (e.g., forecasting monthly case volume)
- Add doctor-level performance scoring
- Package the EDA into an automated PDF/HTML report generated on each run
