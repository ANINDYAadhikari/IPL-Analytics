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

matches = pd.read_csv(r'C:\Users\anind\OneDrive\Desktop\PythonVSC\Project\IPL-Analytics\Data\matches_clean.csv', encoding='latin-1')
deliveries = pd.read_csv(r'C:\Users\anind\OneDrive\Desktop\PythonVSC\Project\IPL-Analytics\Data\deliveries_clean.csv', encoding='latin-1')
print("Dataset Loaded Successfully!\n")



# ================================
# SECTION 1: BATTING ANALYSIS
# ================================

# Q1: Top Run Scorers
# Find the top 10 batsmen with the highest total runs in IPL history

top_runs = deliveries.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False)
print("Top 10 Run Scorers in IPL:\n", top_runs.head(10))



# Q2: Strike Rate Leaders
# Find batsmen with the highest strike rate (minimum 200 balls faced)

runs = deliveries.groupby('batter')['batsman_runs'].sum()
balls = deliveries.groupby('batter')['ball'].count()

sr_df = pd.DataFrame({'runs': runs, 'balls': balls})
sr_df = sr_df[sr_df['balls'] >= 200]                           # Filter: min 200 balls
sr_df['strike_rate'] = (sr_df['runs'] / sr_df['balls']) * 100  # Formula: (runs / balls) * 100

top_sr = sr_df.sort_values(by='strike_rate', ascending=False).head(10)
print("Top 10 Strike Rate Leaders (min 200 balls):\n", top_sr)



# Q3: Boundary Hitters
# Find who has hit the most fours and sixes

boundary_df = deliveries.groupby('batter')['batsman_runs'].agg(
    fours=lambda x: (x == 4).sum(),
    sixes=lambda x: (x == 6).sum()
)
boundary_df['total_boundaries'] = boundary_df['fours'] + boundary_df['sixes']

top_boundaries = boundary_df.sort_values(by='total_boundaries', ascending=False)
print("Top 10 Boundary Hitters:\n", top_boundaries.head(10))



# Q4: Most Consistent Players
# Find batsmen with high total runs AND strike rate above 120

runs = deliveries.groupby('batter')['batsman_runs'].sum()
balls = deliveries.groupby('batter')['ball'].count()

consistency_df = pd.DataFrame({'runs': runs, 'balls': balls})
consistency_df['strike_rate'] = (consistency_df['runs'] / consistency_df['balls']) * 100

consistency_df = consistency_df[(consistency_df['runs'] > 2000) & (consistency_df['strike_rate'] > 120)]  # Filter: runs > 2000 and SR > 120
consistency_df = consistency_df.sort_values(by='runs', ascending=False)

print("Most Consistent Players (runs > 2000 & SR > 120):\n", consistency_df.head(10))



# ================================
# SECTION 2: BOWLING ANALYSIS
# ================================

# Q5: Top Wicket Takers
# Find bowlers with the most wickets in IPL history

wickets = deliveries[deliveries['dismissal_kind'].notna()]  # Keep only dismissal rows
top_wickets = wickets.groupby('bowler')['ball'].count().sort_values(ascending=False)
print("Top 10 Wicket Takers:\n", top_wickets.head(10))



# Q6: Best Economy Bowlers
# Find bowlers with the best economy rate (minimum 200 balls bowled)

balls_bowled = deliveries.groupby('bowler')['ball'].count()
runs_given = deliveries.groupby('bowler')['total_runs'].sum()

eco_df = pd.DataFrame({'balls': balls_bowled, 'runs': runs_given})
eco_df = eco_df[eco_df['balls'] >= 200]                             # Filter: min 200 balls
eco_df['economy'] = (eco_df['runs'] / eco_df['balls']) * 6         # Formula: (runs / balls) * 6

best_eco = eco_df.sort_values(by='economy')                         # Lower economy = better
print("Best Economy Bowlers (min 200 balls):\n", best_eco.head(10))



# Q7: Strike Bowlers
# Find bowlers who take wickets most frequently (lower bowling SR = better)

balls_bowled = deliveries.groupby('bowler')['ball'].count()
wickets_taken = deliveries[deliveries['dismissal_kind'].notna()].groupby('bowler')['ball'].count()

bowling_sr_df = pd.DataFrame({'balls': balls_bowled, 'wickets': wickets_taken}).fillna(0)
bowling_sr_df = bowling_sr_df[bowling_sr_df['wickets'] > 0]
bowling_sr_df['bowling_strike_rate'] = bowling_sr_df['balls'] / bowling_sr_df['wickets']  # Formula: balls / wickets

best_bowling_sr = bowling_sr_df.sort_values(by='bowling_strike_rate')  # Lower = better
print("Best Strike Bowlers:\n", best_bowling_sr.head(10))



# ================================
# SECTION 3: TEAM ANALYSIS
# ================================

# Q8: Most Successful Teams
# Find which teams have won the most matches

most_wins = matches['winner'].value_counts()
print("Most Successful Teams (Total Wins):\n", most_wins)



# Q9: Toss Impact Analysis
# Check if winning the toss increases the chances of winning the match

toss_win = matches['toss_winner'] == matches['winner']
toss_win_pct = (toss_win.sum() / len(toss_win)) * 100

print("Toss Impact Analysis:")
print(f"Toss winner also won the match:, {toss_win_pct:.2f}%")



# Q10: Win Type Analysis
# Find how many matches were won by runs vs wickets

win_type = matches['match_result_type'].value_counts()
print("Match Win Type Distribution:\n", win_type)