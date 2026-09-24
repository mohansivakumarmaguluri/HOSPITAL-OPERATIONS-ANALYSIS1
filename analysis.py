"""
Hospital Case Mix Index (CMI) Analytics
-----------------------------------------
A standalone Python data analytics script that:
  1. Loads a hospital case-level CSV dataset
  2. Cleans the data (duplicates, missing values, type fixes)
  3. Performs exploratory data analysis (EDA)
  4. Saves all charts as image files and prints a readable summary
     to the console / a text report

Run:
    python analysis.py

Author: Mohan
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------------
DATA_PATH = "data/hospital_data.csv"
OUTPUT_DIR = "outputs"
CHARTS_DIR = os.path.join(OUTPUT_DIR, "charts")
SUMMARY_PATH = os.path.join(OUTPUT_DIR, "eda_summary.txt")

sns.set_style("whitegrid")
plt.rcParams["figure.facecolor"] = "white"

os.makedirs(CHARTS_DIR, exist_ok=True)


def log(msg, log_lines):
    """Print to console and also collect for the text summary file."""
    print(msg)
    log_lines.append(msg)


# ------------------------------------------------------------------
# 1. LOAD DATA
# ------------------------------------------------------------------
def load_data(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset not found at '{path}'.")
    return pd.read_csv(path)


# ------------------------------------------------------------------
# 2. CLEAN DATA
# ------------------------------------------------------------------
def clean_data(df: pd.DataFrame, log_lines):
    log("\n=== DATA CLEANING ===", log_lines)
    log(f"Raw dataset shape: {df.shape}", log_lines)

    # Drop fully empty rows
    df = df.dropna(how="all")
    log(f"After dropping fully empty rows: {df.shape}", log_lines)

    # Remove duplicate rows
    dup_count = df.duplicated().sum()
    df = df.drop_duplicates()
    log(f"Duplicate rows removed: {dup_count}", log_lines)
    log(f"After removing duplicates: {df.shape}", log_lines)

    # Standardise column names
    df.columns = [c.strip() for c in df.columns]

    # Parse DOB and engineer Age
    if "DOB" in df.columns:
        df["DOB"] = pd.to_datetime(df["DOB"], format="%d-%m-%Y", errors="coerce")
        today = pd.Timestamp.today()
        df["Age"] = ((today - df["DOB"]).dt.days // 365).astype("Int64")

    # Missing values before
    missing_before = df.isna().sum().sum()
    log(f"\nMissing values before imputation: {missing_before}", log_lines)
    log(str(df.isna().sum()), log_lines)

    # Fill categorical missing values
    cat_cols = ["Nationality", "Gender", "Doctor Type", "Doctor Status", "Month"]
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    # Fill numeric missing values with median
    if "CMI Value" in df.columns:
        df["CMI Value"] = pd.to_numeric(df["CMI Value"], errors="coerce")
        median_cmi = df["CMI Value"].median()
        df["CMI Value"] = df["CMI Value"].fillna(round(median_cmi, 2))

    missing_after = df.isna().sum().sum()
    log(f"\nMissing values after imputation: {missing_after}", log_lines)

    df = df.reset_index(drop=True)
    return df


# ------------------------------------------------------------------
# 3. EXPLORATORY DATA ANALYSIS
# ------------------------------------------------------------------
def run_eda(df: pd.DataFrame, log_lines):
    log("\n=== EXPLORATORY DATA ANALYSIS ===", log_lines)

    # ---- Summary statistics ----
    log("\nSummary statistics (Age, CMI Value):", log_lines)
    log(str(df[["Age", "CMI Value"]].describe().round(2)), log_lines)

    log("\nCase count by Month:", log_lines)
    log(str(df["Month"].value_counts()), log_lines)

    log("\nGender distribution:", log_lines)
    log(str(df["Gender"].value_counts()), log_lines)

    log("\nNationality distribution:", log_lines)
    log(str(df["Nationality"].value_counts()), log_lines)

    log("\nDoctor Type distribution:", log_lines)
    log(str(df["Doctor Type"].value_counts()), log_lines)

    log("\nDoctor Status distribution:", log_lines)
    log(str(df["Doctor Status"].value_counts()), log_lines)

    avg_cmi_by_doctor_type = df.groupby("Doctor Type")["CMI Value"].mean().round(2)
    log("\nAverage CMI Value by Doctor Type:", log_lines)
    log(str(avg_cmi_by_doctor_type), log_lines)

    # ---- Charts ----
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ]

    # 1. Cases by month
    fig, ax = plt.subplots(figsize=(8, 4.5))
    df["Month"].value_counts().reindex(month_order).dropna().plot(
        kind="bar", ax=ax, color="#4C72B0"
    )
    ax.set_title("Cases by Month")
    ax.set_ylabel("Number of Cases")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    fig.savefig(os.path.join(CHARTS_DIR, "01_cases_by_month.png"), dpi=150)
    plt.close(fig)

    # 2. Gender distribution (pie)
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    gender_counts = df["Gender"].value_counts()
    ax.pie(
        gender_counts.values,
        labels=gender_counts.index,
        autopct="%1.1f%%",
        colors=sns.color_palette("pastel"),
        startangle=90,
    )
    ax.set_title("Gender Distribution")
    ax.axis("equal")
    plt.tight_layout()
    fig.savefig(os.path.join(CHARTS_DIR, "02_gender_distribution.png"), dpi=150)
    plt.close(fig)

    # 3. CMI value distribution
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.histplot(df["CMI Value"], bins=20, kde=True, ax=ax, color="#55A868")
    ax.set_title("CMI Value Distribution")
    ax.set_xlabel("CMI Value")
    plt.tight_layout()
    fig.savefig(os.path.join(CHARTS_DIR, "03_cmi_distribution.png"), dpi=150)
    plt.close(fig)

    # 4. CMI value by doctor type (boxplot)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.boxplot(data=df, x="Doctor Type", y="CMI Value", hue="Doctor Type", ax=ax, palette="Set2", legend=False)
    ax.set_title("CMI Value by Doctor Type")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    fig.savefig(os.path.join(CHARTS_DIR, "04_cmi_by_doctor_type.png"), dpi=150)
    plt.close(fig)

    # 5. Nationality breakdown
    fig, ax = plt.subplots(figsize=(8, 4.5))
    nat_counts = df["Nationality"].value_counts()
    sns.barplot(x=nat_counts.values, y=nat_counts.index, hue=nat_counts.index, ax=ax, palette="Blues_r", legend=False)
    ax.set_title("Nationality Breakdown")
    ax.set_xlabel("Number of Cases")
    plt.tight_layout()
    fig.savefig(os.path.join(CHARTS_DIR, "05_nationality_breakdown.png"), dpi=150)
    plt.close(fig)

    # 6. Doctor status breakdown
    fig, ax = plt.subplots(figsize=(7, 4.5))
    status_counts = df["Doctor Status"].value_counts()
    sns.barplot(x=status_counts.index, y=status_counts.values, hue=status_counts.index, ax=ax, palette="Oranges_r", legend=False)
    ax.set_title("Doctor Status Breakdown")
    ax.set_ylabel("Number of Cases")
    plt.tight_layout()
    fig.savefig(os.path.join(CHARTS_DIR, "06_doctor_status_breakdown.png"), dpi=150)
    plt.close(fig)

    # 7. Age distribution
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.histplot(df["Age"].dropna(), bins=20, kde=True, ax=ax, color="#C44E52")
    ax.set_title("Patient Age Distribution")
    ax.set_xlabel("Age")
    plt.tight_layout()
    fig.savefig(os.path.join(CHARTS_DIR, "07_age_distribution.png"), dpi=150)
    plt.close(fig)

    log(f"\nAll charts saved to '{CHARTS_DIR}/'", log_lines)


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
def main():
    log_lines = []

    log("Loading dataset...", log_lines)
    raw_df = load_data(DATA_PATH)

    clean_df = clean_data(raw_df, log_lines)

    # Save the cleaned dataset for reuse
    cleaned_path = os.path.join(OUTPUT_DIR, "hospital_data_cleaned.csv")
    clean_df.to_csv(cleaned_path, index=False)
    log(f"\nCleaned dataset saved to '{cleaned_path}'", log_lines)

    run_eda(clean_df, log_lines)

    with open(SUMMARY_PATH, "w") as f:
        f.write("\n".join(log_lines))
    print(f"\nFull text summary saved to '{SUMMARY_PATH}'")


if __name__ == "__main__":
    main()
