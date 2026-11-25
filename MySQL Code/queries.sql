CREATE DATABASE bank_analytics;
use bank_analytics;
show tables;

-- Total spend and avg transaction per customer
SELECT
    AccountID,
    COUNT(*) AS total_transactions,
    ROUND(SUM(TransactionAmount), 2) AS total_spend,
    ROUND(AVG(TransactionAmount), 2) AS avg_transaction,
    MAX(TransactionAmount) AS max_transaction
FROM transactions
GROUP BY AccountID
ORDER BY total_spend DESC
LIMIT 20;

-- Analyze transaction volume and spending by transaction type
-- Which transaction types generate the most transactions and highest total transaction amounts?
SELECT
    TransactionType,
    COUNT(*) AS transaction_count,
    ROUND(SUM(TransactionAmount), 2) AS total_amount,
    ROUND(AVG(TransactionAmount), 2) AS avg_amount
FROM transactions
GROUP BY TransactionType
ORDER BY total_amount DESC;

-- Month-wise transaction volume and value
SELECT
    MONTHNAME(TransactionDate) AS month,
    COUNT(*) AS total_transactions,
    ROUND(SUM(TransactionAmount), 2) AS monthly_volume
FROM transactions
GROUP BY MONTH(TransactionDate), MONTHNAME(TransactionDate)
ORDER BY MONTH(TransactionDate);

-- How many suspicious transactions per location?
SELECT 
    Location,
    COUNT(*) AS suspicious_count,
    ROUND(SUM(TransactionAmount), 2) AS suspicious_volume
FROM transactions
WHERE IsSuspicious = 1
GROUP BY Location
ORDER BY suspicious_count DESC;

-- Locations with potentially suspicious transactions
-- (amount > 10000 or login attempts > 3)
SELECT
    Location,
    COUNT(*) AS suspicious_count,
    ROUND(SUM(TransactionAmount), 2) AS suspicious_volume
FROM transactions
WHERE TransactionAmount > 10000
   OR LoginAttempts > 3
GROUP BY Location
ORDER BY suspicious_count DESC;

-- Customers with the highest average transaction amounts
SELECT 
    AccountID,
    CustomerAge,
    ROUND(AVG(TransactionAmount), 2) AS avg_spend,
    COUNT(*) AS total_txns
FROM transactions
GROUP BY AccountID, CustomerAge
HAVING COUNT(*) > 2
ORDER BY avg_spend DESC
LIMIT 10;

-- Transaction type breakdown by spending tier
SELECT
    TransactionType,
    CASE
        WHEN TransactionAmount < 1000 THEN 'Low'
        WHEN TransactionAmount BETWEEN 1000 AND 5000 THEN 'Medium'
        ELSE 'High'
    END AS SpendingTier,
    COUNT(*) AS transaction_count,
    ROUND(SUM(TransactionAmount), 2) AS total_amount
FROM transactions
GROUP BY
    TransactionType,
    CASE
        WHEN TransactionAmount < 1000 THEN 'Low'
        WHEN TransactionAmount BETWEEN 1000 AND 5000 THEN 'Medium'
        ELSE 'High'
    END
ORDER BY TransactionType, total_amount DESC;