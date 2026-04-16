CREATE DATABASE ipl_analytics;
SHOW DATABASES;
USE ipl_analytics;
SHOW TABLES;

-- Q1: Total Matches Played
-- Find total number of matches in the dataset
SELECT count(*) AS winner
FROM matches;

-- Q2: List All Teams
-- Get unique team names that have played 
SELECT DISTINCT team1 AS team_name FROM matches
UNION
SELECT DISTINCT team2 FROM matches;

-- Q3: Matches per Season
-- Count how many matches were played each season
SELECT season, COUNT(*) AS total_matches
FROM matches
GROUP BY season
ORDER BY season;

-- Q4: Toss Decision Count
-- How many times teams chose batting vs fielding?
SELECT toss_decision, COUNT(*) AS total_count
FROM matches
GROUP BY toss_decision;

-- Q5: Top 10 Run Scorers
-- Find batsmen with highest total runs
SELECT batter, SUM(batsman_runs) AS total_runs
FROM deliveries
GROUP BY batter
ORDER BY total_runs DESC
LIMIT 10;

-- Q6: Players with Most Matches Played
-- Find players who appeared most frequently
SELECT player_of_match, COUNT(*) AS matches_count
FROM matches
GROUP BY player_of_match
ORDER BY matches_count DESC
LIMIT 10;

-- Q7: Team with Most Wins
-- Find which team has highest wins
SELECT winner, COUNT(*) AS total_wins
FROM matches
WHERE winner != 'No Result'
GROUP BY winner
ORDER BY total_wins DESC
LIMIT 5;

-- Q8: Matches Won by Runs vs Wickets
-- Compare win types
SELECT match_result_type, COUNT(*) AS total_matches
FROM matches
GROUP BY match_result_type;

-- Q9: Toss Impact
-- Does winning toss increase match wins?
SELECT COUNT(*) AS total_matches,
    SUM(CASE 
            WHEN toss_winner = winner THEN 1 
            ELSE 0 
        END) AS toss_win_and_match_win,
    (SUM(CASE 
            WHEN toss_winner = winner THEN 1 
            ELSE 0 
         END) * 100.0 / COUNT(*)) AS win_percentage
FROM matches;

-- Q10: Win % of Each Team
-- Calculate win percentage of every team
SELECT team, total_matches, total_wins,
    ROUND((total_wins * 100.0 / total_matches), 2) AS win_percentage
FROM (
    SELECT 
        team,
        COUNT(*) AS total_matches,
        SUM(CASE 
                WHEN team = winner THEN 1 
                ELSE 0 
            END) AS total_wins
    FROM (
        SELECT team1 AS team, winner FROM matches
        UNION ALL
        SELECT team2 AS team, winner FROM matches
    ) AS all_teams
    GROUP BY team
) AS stats
ORDER BY win_percentage DESC;

-- Q11: Top Bowlers by Wickets
-- Find bowlers with most wickets
SELECT bowler, wickets
FROM bowling_stats
ORDER BY wickets DESC
LIMIT 10;

-- Q12: Economical Bowlers (with condition)
-- Find bowlers with best economy but only if they bowled enough
SELECT 
    bowler,
    COUNT(*) AS balls_bowled,
    SUM(total_runs) AS runs_given,
    ROUND((SUM(total_runs) * 6.0 / COUNT(*)), 2) AS economy
FROM deliveries
GROUP BY bowler
HAVING balls_bowled >= 200
ORDER BY economy ASC
LIMIT 10;