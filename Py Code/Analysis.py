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
matches = pd.read_csv(r'C:\Users\anind\OneDrive\Desktop\PythonVSC\Project\IPL-Analytics\Data\matches_clean.csv', encoding='latin-1')
deliveries = pd.read_csv(r'C:\Users\anind\OneDrive\Desktop\PythonVSC\Project\IPL-Analytics\Data\deliveries_clean.csv', encoding='latin-1')
print("Dataset Loaded Successfully!\n")



'''✅ Q1: Top Run Scorers

👉 Question:
Find the top 10 batsmen with the highest total runs in IPL history.

💡 Hint:

Use groupby('batsman')
Sum batsman_runs
Sort descending'''
'''top_run = deliveries.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False)
print("Top 10 Run Scorers in IPL:\n", top_run.head(10))'''



'''✅ Q2: Strike Rate Leaders

👉 Question:
Which batsmen have the highest strike rate (minimum 200 balls faced)?

💡 Hint:

Count balls using ball
Formula:
strike_rate = (runs / balls) * 100
Filter: balls >= 200'''
'''# Total runs by batter
runs = deliveries.groupby('batter')['batsman_runs'].sum()

# Total balls faced by batter
balls = deliveries.groupby('batter')['ball'].count()

# Combine into one DataFrame
sr_df = pd.DataFrame({
    'runs': runs,
    'balls': balls
})

# Filter players with at least 200 balls
sr_df = sr_df[sr_df['balls'] >= 200]

# Calculate strike rate
sr_df['strike_rate'] = (sr_df['runs'] / sr_df['balls']) * 100

# Sort and get top 10
top_sr = sr_df.sort_values(by='strike_rate', ascending=False).head(10)

print("Top 10 Strike Rate Leaders (min 200 balls):\n", top_sr)'''




'''✅ Q3: Boundary Hitters
👉 Question:
Who has hit the most fours and sixes?
💡 Hint:
Use condition:
(x == 4).sum()
(x == 6).sum()
Add columns: fours, sixes'''
'''# Group by batter and count fours & sixes
boundary_df = deliveries.groupby('batter')['batsman_runs'].agg(
    fours = lambda x: (x == 4).sum(),
    sixes = lambda x: (x == 6).sum()
)

# Sort by total boundaries (optional)
boundary_df['total_boundaries'] = boundary_df['fours'] + boundary_df['sixes']
top_boundary = boundary_df.sort_values(by='total_boundaries', ascending=False)
print("Top Boundary Hitters:\n", top_boundary.head(10))'''




'''✅ Q4: Most Consistent Players
👉 Question:
Which batsmen score consistently (high runs + decent strike rate)?
💡 Hint:
Combine:
High runs
Strike rate > 120
Use filtering after aggregation'''
'''# Total runs
runs = deliveries.groupby('batter')['batsman_runs'].sum()

# Balls faced
balls = deliveries.groupby('batter')['ball'].count()

# Create DataFrame
mcp = pd.DataFrame({
    'runs': runs,
    'balls': balls
})

# Calculate strike rate
mcp['strike_rate'] = (mcp['runs'] / mcp['balls']) * 100

# Filter: high runs + decent strike rate
mcp = mcp[(mcp['runs'] > 2000) & (mcp['strike_rate'] > 120)]

# Sort
mcp = mcp.sort_values(by='runs', ascending=False)

print("Most Consistent Players:\n", mcp.head(10))'''




'''🔹 SECTION 2: BOWLING ANALYSIS
✅ Q5: Top Wicket Takers
👉 Question:
Who has taken the most wickets?
💡 Hint:
Filter rows where dismissal_kind is NOT null
Then:
groupby('bowler').count()'''
'''# Filter only wicket rows
wickets = deliveries[deliveries['dismissal_kind'].notna()]
# Count wickets per bowler
top_wicket = wickets.groupby('bowler')['ball'].count().sort_values(ascending=False)
print(top_wicket.head(10))'''



'''✅ Q6: Best Economy Bowlers
👉 Question:
Which bowlers have the best economy rate (min 200 balls)?
💡 Hint:
Formula:
economy = (runs_given / balls) * 6
Filter: balls >= 200'''
'''# Total balls bowled by each bowler
balls = deliveries.groupby('bowler')['ball'].count()

# Total runs given by each bowler
runs = deliveries.groupby('bowler')['total_runs'].sum()

# Create DataFrame
eco_df = pd.DataFrame({
    'balls': balls,
    'runs': runs
})

# Filter bowlers with at least 200 balls
eco_df = eco_df[eco_df['balls'] >= 200]

# Calculate economy rate
eco_df['economy'] = (eco_df['runs'] / eco_df['balls']) * 6

# Sort (lower economy is better)
best_eco = eco_df.sort_values(by='economy')

print("Best Economy Bowlers (min 200 balls):\n", best_eco.head(10))'''



'''✅ Q7: Strike Bowlers
👉 Question:
Which bowlers take wickets frequently?
💡 Hint:
Bowling strike rate:
balls / wickets
Lower = better'''
'''# Total balls bowled
balls = deliveries.groupby('bowler')['ball'].count()

# Total wickets taken
wickets = deliveries[deliveries['dismissal_kind'].notna()] \
            .groupby('bowler')['ball'].count()

# Create DataFrame
sr_df = pd.DataFrame({
    'balls': balls,
    'wickets': wickets
}).fillna(0)

# Filter bowlers with at least 50 wickets (optional but useful)
sr_df = sr_df[sr_df['wickets'] > 0]

# Calculate strike rate
sr_df['strike_rate'] = sr_df['balls'] / sr_df['wickets']

# Sort (lower is better)
best_sr = sr_df.sort_values(by='strike_rate')

print("Best Strike Bowlers:\n", best_sr.head(10))'''





'''🔹 SECTION 3: TEAM ANALYSIS
✅ Q8: Most Successful Teams
👉 Question:
Which teams have won the most matches?
💡 Hint:
matches['winner'].value_counts()'''
'''most_won = matches['winner'].value_counts()
print("Most Successful Teams (Total Wins):\n", most_won)'''





'''✅ Q9: Toss Impact
👉 Question:
Does winning the toss increase chances of winning the match?
💡 Hint:
Compare:
matches['toss_winner'] == matches['winner']
Calculate percentage'''
'''win = matches['toss_winner'] == matches['winner']
# Calculate percentage
percentage = (win.sum() / len(win)) * 100
print("Toss Impact Analysis:\n")
print("Percentage of matches where toss winner also won:", percentage, "%")'''




'''✅ Q10: Win Type Analysis
👉 Question:
How many matches are won by runs vs wickets?
💡 Hint:
Use your column:
match_result_type
Apply value_counts()'''
win_type = matches['match_result_type'].value_counts()
print("Match Win Type Distribution:\n", win_type)