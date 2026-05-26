# =========================
# IPL DATA ANALYSIS PROJECT
# -------------------------
# Author -- Anindya Adhikari
# =========================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8')

# Load Dataset
matches = pd.read_csv(r"C:\Project\IPL-Analytics\Data\matches.csv", encoding='latin-1')
deliveries = pd.read_csv(r"C:\Project\IPL-Analytics\Data\deliveries.csv", encoding='latin-1')
print("Dataset Loaded Successfully!\n")



# Q1: Missing Value Audit
# Before doing any analysis, it's important to know which columns have missing data.
# Here we calculate the missing count and percentage for both datasets.

# Matches
nan_value_matches = matches.isnull().sum()
nan_percentage_matches = (nan_value_matches / len(matches)) * 100

missing_matches = pd.DataFrame({
    'column_name': nan_value_matches.index,
    'missing_count': nan_value_matches.values,
    'missing_percentage': nan_percentage_matches.values
}).sort_values(by='missing_percentage', ascending=False)

print("Matches Missing Value Audit:\n", missing_matches)

# Deliveries
nan_value_deliveries = deliveries.isnull().sum()
nan_percentage_deliveries = (nan_value_deliveries / len(deliveries)) * 100

missing_deliveries = pd.DataFrame({
    'column_name': nan_value_deliveries.index,
    'missing_count': nan_value_deliveries.values,
    'missing_percentage': nan_percentage_deliveries.values
}).sort_values(by='missing_percentage', ascending=False)

print("\nDeliveries Missing Value Audit:\n", missing_deliveries)



# Q2: Drop Irrelevant Columns
# Umpire columns are not needed for our analysis.
# Instead of dropping them one by one, we find them dynamically using a loop.

umpire_cols = [col for col in matches.columns if "umpire" in col.lower()]
matches = matches.drop(columns=umpire_cols)
print("Remaining columns after dropping umpire cols:", matches.shape[1])



# Q3: Standardize Team Names
# Over the years, several IPL teams were renamed.
# We fix these inconsistencies by mapping old names to their current official names.

team_name_map = {
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru",
    "Deccan Chargers": "Sunrisers Hyderabad",
    "Kings XI Punjab": "Punjab Kings",
    "Delhi Daredevils": "Delhi Capitals",
    "Rising Pune Supergiant": "Rising Pune Supergiants",  # Typo fix
    "Gujarat Lions": "Gujarat Titans",
    "Kolkata Knight Riders": "Kolkata Knight Riders",
    "Chennai Super Kings": "Chennai Super Kings",
    "Rajasthan Royals": "Rajasthan Royals",
    "Mumbai Indians": "Mumbai Indians",
    "Kochi Tuskers Kerala": "Kochi Tuskers Kerala",
    "Pune Warriors": "Pune Warriors",
    "Sunrisers Hyderabad": "Sunrisers Hyderabad",
    "Rising Pune Supergiants": "Rising Pune Supergiants",
    "Delhi Capitals": "Delhi Capitals",
    "Punjab Kings": "Punjab Kings",
    "Gujarat Titans": "Gujarat Titans",
    "Lucknow Super Giants": "Lucknow Super Giants"
}

matches[['team1', 'team2', 'winner', 'toss_winner']] = \
    matches[['team1', 'team2', 'winner', 'toss_winner']].replace(team_name_map)

print("\nTeam names standardized successfully!")



# Q4: Handle Missing Values Smartly
# Not all missing values should be treated the same way.
# We fill some columns with meaningful defaults and drop rows where the data truly can't be recovered.

matches["winner"] = matches["winner"].fillna("No Result")
matches["player_of_match"] = matches["player_of_match"].fillna("Unknown")
matches = matches.dropna(subset=["city"])  # Rows without city info are dropped

print("\nNull values remaining:\n", matches.isna().sum())



# Q5: Remove Duplicate Records
# Duplicate rows can skew our analysis results.
# We check and remove them from both datasets.

matches_duplicates = matches.duplicated().sum()
deliveries_duplicates = deliveries.duplicated().sum()

matches = matches.drop_duplicates()
deliveries = deliveries.drop_duplicates()

print(f"Duplicates removed -> Matches: {matches_duplicates} | Deliveries: {deliveries_duplicates}")



# Q6: Data Type Optimization
# Columns like 'season' and 'date' are stored as strings by default.
# Converting them to proper types makes sorting, filtering, and calculations easier.

matches["season"] = matches["season"].astype(str).str.extract(r'(\d{4})')[0].astype(int)
matches["date"] = pd.to_datetime(matches["date"])

numeric_cols = ["match_id", "inning", "over", "ball", "batsman_runs", "extra_runs", "total_runs", "is_wicket"]
for col in numeric_cols:
    deliveries[col] = pd.to_numeric(deliveries[col], errors="coerce")



# Q7: Outlier Detection
# We check for values in 'result_margin' that don't make logical sense --
# like negative margins or wicket wins greater than 10 (max wickets in cricket is 10).

print("Negative result_margin:\n", matches[matches["result_margin"] < 0])
print("\nWicket wins greater than 10:\n", matches[matches["result_margin"] > 10])



# Q8: Create match_result_type Column
# The 'result' column only stores 'runs' or 'wickets' as raw text.
# We create a cleaner column 'match_result_type' for better readability in analysis.

matches["match_result_type"] = "No Result"
matches.loc[matches["result"] == "runs", "match_result_type"] = "Runs"
matches.loc[matches["result"] == "wickets", "match_result_type"] = "Wickets"



# Q9: Validate Winner Column
# We verify that every match winner is either team1, team2, or 'No Result'.
# Any other value would indicate a data quality issue.

valid_winners = matches[
    (matches["winner"] == matches["team1"]) |
    (matches["winner"] == matches["team2"]) |
    (matches["winner"] == "No Result")
]
print(f"\nTotal valid winner rows: {len(valid_winners)} / {len(matches)}")



# Save cleaned versions to data folder
matches.to_csv(r'C:\Users\anind\OneDrive\Desktop\PythonVSC\Project\IPL-Analytics\Data\matches_clean.csv', index=False)
deliveries.to_csv(r'C:\Users\anind\OneDrive\Desktop\PythonVSC\Project\IPL-Analytics\Data\deliveries_clean.csv', index=False)

print("Cleaned files saved.")
