# =========================
# E-COMMERCE SALES ANALYSIS
# -------------------------
# Author-- Anindya Adhikari
# =========================

# Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

plt.style.use('seaborn-v0_8')

# Load Dataset
matches = pd.read_csv(r"C:\Users\anind\OneDrive\Desktop\PythonVSC\Project\IPL-Analytics\Data\matches.csv", encoding='latin-1') 
deliveries = pd.read_csv(r"C:\Users\anind\OneDrive\Desktop\PythonVSC\Project\IPL-Analytics\Data\deliveries.csv", encoding='latin-1') 
print("Dataset Loaded Successfully!\n")



# Q1: Missing Value Audit 
# Write code to: Calculate total missing values per column 
# Calculate percentage of missing values Combine both into a single DataFrame 
# Sort descending by percentage

# MATCHES DATASET
nan_value_matches = matches.isnull().sum()  # Missing count
nan_percentage_matches = (nan_value_matches / len(matches)) * 100  # Missing percentage
missing_matches = pd.DataFrame({  # Combine into DataFrame
    'column_name': nan_value_matches.index,
    'missing_count': nan_value_matches.values,
    'missing_percentage': nan_percentage_matches.values
})
missing_matches = missing_matches.sort_values(by='missing_percentage', ascending=False)  # Sort
print("\nMatches Missing Value Audit:\n", missing_matches)

# DELIVERIES DATASET
# Missing count
nan_value_deliveries = deliveries.isnull().sum()
# Missing percentage
nan_percentage_deliveries = (nan_value_deliveries / len(deliveries)) * 100
# Combine into DataFrame
missing_deliveries = pd.DataFrame({
    'column_name': nan_value_deliveries.index,
    'missing_count': nan_value_deliveries.values,
    'missing_percentage': nan_percentage_deliveries.values
})
# Sort
missing_deliveries = missing_deliveries.sort_values(by='missing_percentage', ascending=False)
print("\nDeliveries Missing Value Audit:\n", missing_deliveries)


# Q2: Drop Irrelevant Columns
# From matches:
# Drop all umpire-related columns dynamically 
# Print remaining column count
umpire_cols = []
for col in matches.columns:
    if "umpire" in col.lower():
        umpire_cols.append(col)
matches = matches.drop(columns = umpire_cols)
print("Remaining columns:", matches.shape[1])


# Q3: Standardize Team Names 
# Clean inconsistent team names
# Replace old names with new ones
# Get all unique team names
for col in ['team1', 'team2', 'winner', 'toss_winner']:
    print(f"\n{col} unique values:\n", matches[col].unique())

team_name_map = {
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru",
    "Kolkata Knight Riders": "Kolkata Knight Riders",

    "Chennai Super Kings": "Chennai Super Kings",
    "Rajasthan Royals": "Rajasthan Royals",
    "Mumbai Indians": "Mumbai Indians",
    "Deccan Chargers": "Sunrisers Hyderabad",
    "Kings XI Punjab": "Punjab Kings",
    "Delhi Daredevils": "Delhi Capitals",
    "Kochi Tuskers Kerala": "Kochi Tuskers Kerala",
    "Pune Warriors": "Pune Warriors",
    "Sunrisers Hyderabad": "Sunrisers Hyderabad",
    "Gujarat Lions": "Gujarat Titans",
    "Rising Pune Supergiants": "Rising Pune Supergiants",
    "Rising Pune Supergiant": "Rising Pune Supergiants",
    "Delhi Capitals": "Delhi Capitals",
    "Punjab Kings": "Punjab Kings",
    "Gujarat Titans": "Gujarat Titans",
    "Lucknow Super Giants": "Lucknow Super Giants"
}
matches[['team1', 'team2', 'winner', 'toss_winner']] = \
    matches[['team1', 'team2', 'winner', 'toss_winner']].replace(team_name_map)
# Print unique team names after changes
print("\nAfter standardizing:\n")
for col in ['team1', 'team2', 'winner', 'toss_winner']:
    print(f"\n{col} unique values:\n", matches[col].unique())


# Q4: Handle Missing Values Smartly
# Fill missing values
matches["winner"] = matches["winner"].fillna("No Result")
matches["player_of_match"] = matches["player_of_match"].fillna("Unknown")
# Drop rows where city is missing
matches = matches.dropna(subset=["city"])
# Check remaining null values
print(matches.isna().sum())


# Q5: Remove Duplicate Records
# Check duplicates in both datasets
# Remove them if present
# Print number of duplicates removed
matches_duplicates = matches.duplicated().sum()
deliveries_duplicates = deliveries.duplicated().sum()

matches = matches.drop_duplicates()
deliveries = deliveries.drop_duplicates()

print("Duplicates removed from matches:", matches_duplicates)
print("Duplicates removed from deliveries:", deliveries_duplicates)



# Q6: Data Type Optimization
# Convert season to integer (extract year if needed)
matches["season"] = matches["season"].astype(str).str.extract(r'(\d{4})')[0].astype(int)

# Convert date to datetime format
matches["date"] = pd.to_datetime(matches["date"])


# Convert numeric columns in deliveries dataset
numeric_cols = [
    "match_id", "inning", "over", "ball",
    "batsman_runs", "extra_runs", "total_runs", "is_wicket"
]

for col in numeric_cols:
    deliveries[col] = pd.to_numeric(deliveries[col], errors="coerce")


# Q7: Outlier Detection
# Matches where result_margin < 0
print("Negative result_margin:\n", matches[matches["result_margin"] < 0])

# Matches where result_margin > 10 (wickets case)
print("\nWickets > 10:\n", matches[matches["result_margin"] > 10])



# Q8: Create match_result_type column

matches["match_result_type"] = "No Result"

# If win by runs
matches.loc[matches["result"] == "runs", "match_result_type"] = "Runs"

# If win by wickets
matches.loc[matches["result"] == "wickets", "match_result_type"] = "Wickets"



# Q9: Check invalid winners

invalid_rows = matches[
    (
        (matches["winner"] == matches["team1"]) |
        (matches["winner"] == matches["team2"]) |
        (matches["winner"] == "No Result")
    )
]

print("Invalid rows:\n", invalid_rows)