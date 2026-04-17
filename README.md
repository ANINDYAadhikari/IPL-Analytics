# 🏏 IPL Analytics — End-to-End Data Analytics Project

A complete data analytics project on the Indian Premier League (IPL), covering everything from raw data cleaning to an interactive Power BI dashboard. Built using Python, MySQL, and Power BI.

---

## 📌 Project Overview

Cricket is more than a sport in India — it's an emotion. And the IPL, with over 15 years of high-intensity T20 cricket, produces a goldmine of data. This project digs into that data to uncover real patterns: which batsmen consistently perform under pressure, which bowlers are the most economical, and whether winning the toss actually matters as much as people think.

The goal was simple — take raw ball-by-ball data and turn it into something that actually tells a story.

---

## 🗂️ Repository Structure

```
IPL-Analytics/
│
├── Data/               ← Raw and cleaned CSV files (matches & deliveries)
├── Images/             ← All chart outputs saved as PNG
├── MySQL Code/         ← SQL queries for analysis
├── Power BI/           ← .pbix dashboard file
└── Py Code/            ← Python scripts for cleaning, analysis & visualization
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python (Pandas, NumPy) | Data cleaning and statistical analysis |
| Matplotlib & Seaborn | Static visualizations and charts |
| MySQL | Data storage and SQL-based analysis |
| SQLAlchemy | Connecting Python to MySQL |
| Power BI | Interactive dashboard |

---

## 📦 Dataset

- **Source:** [Kaggle — IPL Complete Dataset](https://www.kaggle.com/datasets/nowke9/ipldata)
- **Files:** `matches.csv` and `deliveries.csv`
- **Coverage:** IPL seasons from 2008 onwards
- `matches.csv` — match-level data (teams, venue, toss, result, player of the match)
- `deliveries.csv` — ball-by-ball data (batsman, bowler, runs, wickets, extras)

---

## 🔍 What I Analyzed

### 🏏 Batting
- Top 10 all-time run scorers
- Strike rate comparison among top batsmen
- Boundary percentage (4s and 6s) by player

### 🎯 Bowling
- Top 10 wicket takers in IPL history
- Most economical bowlers (min. 200 balls bowled)
- Bowlers with best wickets-per-match ratio

### 🏆 Team Performance
- Total wins by each franchise across all seasons
- Win percentage with and without toss advantage
- Toss decision breakdown — bat vs field

### 🤔 Interesting Questions
- Does winning the toss actually help you win the match?
- Which team has the most consistent win rate?
- Who has won the most Player of the Match awards?

---

## 📊 Visualizations

All charts are saved in the `Images/` folder. Here's a quick summary of what's included:

- **Top 10 Run Scorers** — bar chart ranked by total runs
- **Top 10 Wicket Takers** — bar chart ranked by total wickets
- **Team Wins** — horizontal bar showing all-time wins per franchise
- **Toss Impact** — pie chart showing whether toss winners go on to win the match

---

## 🗄️ MySQL Integration

Cleaned DataFrames were pushed directly to a local MySQL database (`ipl_analytics`) using SQLAlchemy. The following tables were created:

- `matches` — cleaned match-level data
- `deliveries` — ball-by-ball data
- `batting_stats` — aggregated batting stats per player
- `bowling_stats` — aggregated bowling stats per player

Key SQL queries written (available in `MySQL Code/`):

```sql
-- Top 5 run scorers
SELECT batsman, runs, strike_rate FROM batting_stats ORDER BY runs DESC LIMIT 5;

-- Win % by team
SELECT winner AS team, COUNT(*) AS wins,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM matches), 2) AS win_pct
FROM matches WHERE winner != 'No Result'
GROUP BY winner ORDER BY wins DESC;

-- Does the toss help?
SELECT toss_decision, COUNT(*) AS total,
       SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) AS won_match
FROM matches GROUP BY toss_decision;
```

---

## 📈 Power BI Dashboard

The `.pbix` file is in the `Power BI/` folder. The dashboard has 3 pages:

| Page | What's on it |
|------|-------------|
| Overview | Total matches, total runs, wins by team |
| Batting | Top run scorers, strike rates, season trends |
| Bowling | Top wicket takers, economy rates |


**Slicers available:** Season, Team, and Player — so you can drill down into any specific combination.

To open it: download the `.pbix` file → open in Power BI Desktop → connect to your local MySQL instance if needed, or use the embedded data.

---

## ▶️ How to Run the Python Code

1. Clone this repository
```bash
git clone https://github.com/ANINDYAadhikari/IPL-Analytics.git
cd IPL-Analytics
```

2. Install dependencies
```bash
pip install pandas numpy matplotlib seaborn sqlalchemy mysql-connector-python
```

3. Place `matches.csv` and `deliveries.csv` inside the `Data/` folder

4. Update the MySQL credentials in the script:
```python
engine = create_engine('mysql+mysqlconnector://root:yourpassword@localhost/ipl_analytics')
```

5. Run the script
```bash
python "Py Code/analysis.py"
```

---

## 💡 Key Insights

- **Mumbai Indians** have the highest number of wins across all seasons
- Toss winners win roughly **50% of the time** — so the toss matters less than you'd think
- **Virat Kohli** leads the all-time run charts with a significant margin
- Bowlers who field first tend to have better economy rates in the death overs
- **Chennai Super Kings** are consistently the most efficient team by win percentage

---

## 🚀 Skills Demonstrated

- Data cleaning and preprocessing with Pandas
- Aggregation and feature engineering (strike rate, economy, win %)
- Data visualization using Matplotlib and Seaborn
- Relational database design and SQL querying in MySQL
- Building multi-page interactive dashboards in Power BI
- End-to-end project structure and documentation

---

## 🙋 About Me

I'm a data analytics enthusiast who enjoys turning raw datasets into meaningful stories. This is my third portfolio project — previous ones include an E-Commerce Sales Analysis and a Suicide Rate Analysis. Always open to feedback and suggestions!

Connect with me on [LinkedIn](https://www.linkedin.com/in/anindya-adhikari-55aa89239/) | [GitHub](https://github.com/ANINDYAadhikari)

---

*Dataset credit: Kaggle IPL Dataset | Tools: Python, MySQL, Power BI*