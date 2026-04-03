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

# Plot a bar chart of top 10 batsmen by total runs
# Question: Who are the highest run scorers in IPL history?  ANS = Virat Kohli 
plt.figure(figsize=(10, 5))
top_runs.head(10).plot(kind='bar', color='steelblue')
plt.title("Top 10 Run Scorers in IPL")
plt.xlabel("Batsman")
plt.ylabel("Total Runs")
plt.xticks(rotation=35, ha='right')
plt.tight_layout()
plt.show()



# Q2: Strike Rate Leaders
# Find batsmen with the highest strike rate (minimum 200 balls faced)

runs = deliveries.groupby('batter')['batsman_runs'].sum()
balls = deliveries.groupby('batter')['ball'].count()

sr_df = pd.DataFrame({'runs': runs, 'balls': balls})
sr_df = sr_df[sr_df['balls'] >= 200]                           # Filter: min 200 balls
sr_df['strike_rate'] = (sr_df['runs'] / sr_df['balls']) * 100  # Formula: (runs / balls) * 100

top_sr = sr_df.sort_values(by='strike_rate', ascending=False).head(10)
print("Top 10 Strike Rate Leaders (min 200 balls):\n", top_sr)

# Plot a bar chart of top 10 batsmen by strike rate
# Question: Which players score runs the fastest?  ANS = PD Salt
plt.figure(figsize=(10, 5))
top_sr['strike_rate'].plot(kind='bar', color='mediumseagreen')
plt.title("Top 10 Strike Rate Leaders (min 200 balls)")
plt.xlabel("Batsman")
plt.ylabel("Strike Rate")
plt.xticks(rotation=35, ha='right')
plt.tight_layout()
plt.show()



# Q3: Boundary Hitters
# Find who has hit the most fours and sixes

boundary_df = deliveries.groupby('batter')['batsman_runs'].agg(
    fours=lambda x: (x == 4).sum(),
    sixes=lambda x: (x == 6).sum()
)
boundary_df['total_boundaries'] = boundary_df['fours'] + boundary_df['sixes']

top_boundaries = boundary_df.sort_values(by='total_boundaries', ascending=False)
print("Top 10 Boundary Hitters:\n", top_boundaries.head(10))

# Plot a grouped bar chart
# Question: Who hits more boundaries and what type (4s vs 6s)?  ANS = Virat Kohli Scored more Sixes than anyone else and Sikhar Dhawan scored more Fours than anyone else
top10 = top_boundaries.head(10)[['fours', 'sixes']]
plt.figure(figsize=(10, 5))
top10.plot(kind='bar', color=['steelblue', 'tomato'])
plt.title("Top 10 Boundary Hitters (Fours vs Sixes)")
plt.xlabel("Batsman")
plt.ylabel("Count")
plt.xticks(rotation=35, ha='right')
plt.tight_layout()
plt.show()




# Q4: Most Consistent Players
# Find batsmen with high total runs AND strike rate above 120

runs = deliveries.groupby('batter')['batsman_runs'].sum()
balls = deliveries.groupby('batter')['ball'].count()

consistency_df = pd.DataFrame({'runs': runs, 'balls': balls})
consistency_df['strike_rate'] = (consistency_df['runs'] / consistency_df['balls']) * 100

consistency_df = consistency_df[(consistency_df['runs'] > 2000) & (consistency_df['strike_rate'] > 120)]  # Filter: runs > 2000 and SR > 120
consistency_df = consistency_df.sort_values(by='runs', ascending=False)

print("Most Consistent Players (runs > 2000 & SR > 120):\n", consistency_df.head(10))


# Plot a scatter plot
# Question: Which players balance high runs and high strike rate?  ANS = Virat Kohli 
plt.figure(figsize=(9, 5))
plt.scatter(consistency_df['strike_rate'], consistency_df['runs'], color='steelblue', alpha=0.7)
plt.title("Most Consistent Players (Runs vs Strike Rate)")
plt.xlabel("Strike Rate")
plt.ylabel("Total Runs")
plt.tight_layout()
plt.show()




# ================================
# SECTION 2: BOWLING ANALYSIS
# ================================

# Q5: Top Wicket Takers
# Find bowlers with the most wickets in IPL history

wickets = deliveries[deliveries['dismissal_kind'].notna()]  # Keep only dismissal rows
top_wickets = wickets.groupby('bowler')['ball'].count().sort_values(ascending=False)
print("Top 10 Wicket Takers:\n", top_wickets.head(10))

# Plot a bar chart of top 10 wicket takers
# Question: Who are the most successful bowlers in IPL history?   ANS =   YS Chahal 
plt.figure(figsize=(10, 5))
top_wickets.head(10).plot(kind='bar', color='salmon')
plt.title("Top 10 Wicket Takers in IPL")
plt.xlabel("Bowler")
plt.ylabel("Wickets")
plt.xticks(rotation=35, ha='right')
plt.tight_layout()
plt.show()



# Q6: Best Economy Bowlers
# Find bowlers with the best economy rate (minimum 200 balls bowled)

balls_bowled = deliveries.groupby('bowler')['ball'].count()
runs_given = deliveries.groupby('bowler')['total_runs'].sum()

eco_df = pd.DataFrame({'balls': balls_bowled, 'runs': runs_given})
eco_df = eco_df[eco_df['balls'] >= 200]                             # Filter: min 200 balls
eco_df['economy'] = (eco_df['runs'] / eco_df['balls']) * 6         # Formula: (runs / balls) * 6

best_eco = eco_df.sort_values(by='economy')                         # Lower economy = better
print("Best Economy Bowlers (min 200 balls):\n", best_eco.head(10))

# Plot a bar chart of best economy bowlers
# Question: Which bowlers are the most economical?   ANS = Sohail Tanvir  
plt.figure(figsize=(10, 5))
best_eco.head(10)['economy'].plot(kind='bar', color='mediumseagreen')
plt.title("Top 10 Most Economical Bowlers")
plt.xlabel("Bowler")
plt.ylabel("Economy Rate")
plt.xticks(rotation=35, ha='right')
plt.tight_layout()
plt.show()



# Q7: Strike Bowlers
# Find bowlers who take wickets most frequently (lower bowling SR = better)

balls_bowled = deliveries.groupby('bowler')['ball'].count()
wickets_taken = deliveries[deliveries['dismissal_kind'].notna()].groupby('bowler')['ball'].count()

bowling_sr_df = pd.DataFrame({'balls': balls_bowled, 'wickets': wickets_taken}).fillna(0)
bowling_sr_df = bowling_sr_df[bowling_sr_df['wickets'] > 0]
bowling_sr_df['bowling_strike_rate'] = bowling_sr_df['balls'] / bowling_sr_df['wickets']  # Formula: balls / wickets

best_bowling_sr = bowling_sr_df.sort_values(by='bowling_strike_rate')  # Lower = better
print("Best Strike Bowlers:\n", best_bowling_sr.head(10))


# Plot a scatter plot
# Question: Which bowlers are both economical and take wickets quickly?  ANS = AC Gilchrist  

# Merge with strike rate data
final_df = bowling_sr_df.merge(eco_df[['economy']], left_index=True, right_index=True)
plt.figure(figsize=(9, 5))
plt.scatter(final_df['economy'], final_df['bowling_strike_rate'], color='steelblue', alpha=0.6)
plt.title("Bowler Analysis (Economy vs Strike Rate)")
plt.xlabel("Economy Rate")
plt.ylabel("Bowling Strike Rate")
plt.tight_layout()
plt.show()



# ================================
# SECTION 3: TEAM ANALYSIS
# ================================

# Q8: Most Successful Teams
# Find which teams have won the most matches

most_wins = matches['winner'].value_counts()
print("Most Successful Teams (Total Wins):\n", most_wins)

# Plot a horizontal bar chart of total wins
# Question: Which teams have dominated IPL historically?   ANS = Mumbai Indians
plt.figure(figsize=(9, 6))
most_wins.plot(kind='barh', color='steelblue')
plt.title("Total Wins by Teams in IPL")
plt.xlabel("Wins")
plt.ylabel("Team")
plt.tight_layout()
plt.show()



# Q9: Toss Impact Analysis
# Check if winning the toss increases the chances of winning the match

toss_win = matches['toss_winner'] == matches['winner']
toss_win_pct = (toss_win.sum() / len(toss_win)) * 100

print("Toss Impact Analysis:")
print(f"Toss winner also won the match:, {toss_win_pct:.2f}%")

# Plot a pie chart: Toss winner won vs lost
# Question: Does winning the toss significantly affect match results?    ANS = Yes, winning the toss significantly affect match results 
plt.figure(figsize=(7, 6))
toss_counts = toss_win.value_counts()
toss_counts.plot(kind='pie', autopct='%1.1f%%',
                 colors=['steelblue', 'salmon'],
                 wedgeprops={'edgecolor': 'white'})
plt.title("Toss Impact on Match Result")
plt.ylabel("")  # remove default label
plt.tight_layout()
plt.show()



# Q10: Win Type Analysis
# Find how many matches were won by runs vs wickets

win_type = matches['match_result_type'].value_counts()
print("Match Win Type Distribution:\n", win_type)

# Plot: Pie chart of win types
# Question: Are matches usually won by chasing or defending?   ANS = Chasing
plt.figure(figsize=(7, 6))
win_type.plot(kind='pie', autopct='%1.1f%%',
              colors=['mediumseagreen', 'tomato', 'steelblue'],
              wedgeprops={'edgecolor': 'white'})
plt.title("Win Type Distribution (Runs vs Wickets)")
plt.ylabel("")
plt.tight_layout()
plt.show()





# Q1: Top Run Scorers



# Q2: Strike Rate Leaders



# Q3: Boundary Hitters



# Q4: Most Consistent Players



# Q5: Top Wicket Takers



# Q6: Best Economy Bowlers



# Q7: Strike Bowlers



# Q8: Most Successful Teams



# Q9: Toss Impact Analysis



# Q10: Win Type Analysis
