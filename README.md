# 🏥 Hospital Case Mix Index (CMI) Analytics

A complete, beginner-friendly **data analytics project** built with Python.
It loads a hospital case-level dataset, cleans it, performs exploratory data
analysis (EDA), and outputs readable charts and a text summary — all from a
single script.

---

## 📌 Project Overview

Hospitals track a "Case Mix Index" (CMI) to understand the complexity of the
cases they handle. This project analyzes case-level records — patient
demographics, the treating doctor, and the CMI value of each case — to surface
patterns such as:

- How case volume changes month to month
- How CMI values vary across doctor types
- The demographic mix of patients (gender, nationality, age)
- Doctor activity status across the hospital

---

## 🗂️ Project Structure

```
hospital-cmi-analytics/
├── analysis.py             # Main Python script: data loading, cleaning, EDA
├── requirements.txt         # Python dependencies
├── README.md                 # This file
├── PROJECT_REPORT.md         # Detailed project report
├── data/
│   └── hospital_data.csv     # Dataset used by the script
└── outputs/                  # Generated after running the script
    ├── hospital_data_cleaned.csv
    ├── eda_summary.txt
    └── charts/
        ├── 01_cases_by_month.png
        ├── 02_gender_distribution.png
        ├── 03_cmi_distribution.png
        ├── 04_cmi_by_doctor_type.png
        ├── 05_nationality_breakdown.png
        ├── 06_doctor_status_breakdown.png
        └── 07_age_distribution.png
```

---

## 📊 Dataset

The dataset (`data/hospital_data.csv`) contains the following columns:

| Column          | Description                                  |
|-----------------|-----------------------------------------------|
| Month           | Month the case was recorded                   |
| Case_No         | Unique case identifier                         |
| DOB             | Patient date of birth                          |
| Nationality     | Patient nationality                            |
| Gender          | Patient gender                                 |
| DoctorLicense   | Treating doctor's license number               |
| DoctorName      | Treating doctor's name                         |
| Doctor Type     | General Physician / Specialist / Surgeon / Consultant |
| Doctor Status   | Active / Inactive / On Leave                   |
| CMI Value       | Case Mix Index value for the case              |

> **Note:** The dataset shipped in this repo is a **synthetically generated**
> sample created to demonstrate the full pipeline (it intentionally includes
> duplicate rows and missing values so the cleaning step has real work to do).
> You can replace `data/hospital_data.csv` with any real dataset that follows
> the same column structure — no code changes needed.

---

## ⚙️ Features

1. **Data Loading** — reads the raw CSV using Pandas
2. **Data Cleaning**
   - Drops fully empty rows
   - Removes duplicate records
   - Fills missing categorical values as `"Unknown"`
   - Fills missing numeric values with the column median
   - Parses `DOB` and engineers an `Age` column
   - Saves the cleaned dataset to `outputs/hospital_data_cleaned.csv`
3. **Exploratory Data Analysis (EDA)**
   - Case volume by month
   - CMI value distribution
   - CMI value by doctor type
   - Gender & nationality breakdowns
   - Doctor status breakdown
   - Patient age distribution
   - Summary statistics
4. **Readable Output**
   - All charts saved as `.png` files in `outputs/charts/`
   - A full text summary of every statistic printed to the console and
     saved to `outputs/eda_summary.txt`

---

## 🚀 How to Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/hospital-cmi-analytics.git
   cd hospital-cmi-analytics
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the analysis script**
   ```bash
   python analysis.py
   ```

5. Check the `outputs/` folder for:
   - `hospital_data_cleaned.csv` — the cleaned dataset
   - `eda_summary.txt` — a full text summary of the analysis
   - `charts/` — all EDA charts as PNG images

---

## 🛠️ Tech Stack

- **Python** — core language
- **Pandas / NumPy** — data cleaning & manipulation
- **Matplotlib / Seaborn** — visualizations

---

## 📄 Project Report

See [`PROJECT_REPORT.md`](PROJECT_REPORT.md) for the detailed write-up
(objective, methodology, findings, and conclusion).

---

## 👤 Author

**Mohan** — Final-year B.Tech ECE student, aspiring Data Analyst / AI-GenAI professional.

---

## 📃 License

This project is open-sourced for educational and portfolio purposes.
