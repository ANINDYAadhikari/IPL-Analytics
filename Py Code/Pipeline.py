# =========================
# IPL DATA → MySQL PIPELINE
# =========================


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine


matches = pd.read_csv(r'C:\Users\anind\OneDrive\Desktop\PythonVSC\Project\IPL-Analytics\Data\matches_clean.csv', encoding='latin-1')
deliveries = pd.read_csv(r'C:\Users\anind\OneDrive\Desktop\PythonVSC\Project\IPL-Analytics\Data\deliveries_clean.csv', encoding='latin-1')
print("Dataset Loaded Successfully!\n")


# STEP 1: CREATE BATTING STATS

batting = deliveries.groupby('batter').agg({
    'batsman_runs': 'sum',
    'ball': 'count'
}).reset_index()
batting.rename(columns={
    'batsman_runs': 'total_runs',
    'ball': 'balls_faced'
}, inplace=True)

# Strike Rate
batting['strike_rate'] = (batting['total_runs'] / batting['balls_faced']) * 100
print("Batting Stats Created")


# STEP 2: CREATE BOWLING STATS

bowling = deliveries.groupby('bowler').agg({
    'is_wicket': 'sum',
    'ball': 'count',
    'total_runs': 'sum'
}).reset_index()
bowling.rename(columns={
    'is_wicket': 'wickets',
    'ball': 'balls_bowled',
    'total_runs': 'runs_conceded'
}, inplace=True)
print("Bowling Stats Created")


# STEP 3: CONNECT TO MYSQL
engine = create_engine('mysql+mysqlconnector://root:root@localhost/ipl_analytics')
print("Connected to MySQL")


# STEP 4: PUSH DATA TO MYSQL


# Matches Table
matches.to_sql(
    'matches',
    con=engine,
    if_exists='replace',
    index=False
)

print("matches table loaded")

# Deliveries Table (BIG DATA → use chunks)
print("Loading deliveries table... (this may take 1-3 minutes)")
deliveries.to_sql(
    'deliveries',
    con=engine,
    if_exists='replace',
    index=False,
    chunksize=2000,     # smaller = safer
    method='multi'      # faster insert
)

print("deliveries table loaded")


# Batting Stats Table
batting.to_sql(
    'batting_stats',
    con=engine,
    if_exists='replace',
    index=False
)

print("batting_stats table loaded")

# Bowling Stats Table
bowling.to_sql(
    'bowling_stats',
    con=engine,
    if_exists='replace',
    index=False
)

print("bowling_stats table loaded")
print("\n ALL DATA SUCCESSFULLY PUSHED TO MYSQL")