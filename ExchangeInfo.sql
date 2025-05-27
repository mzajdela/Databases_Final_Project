DROP DATABASE IF EXISTS ExchangeInfo;
CREATE DATABASE ExchangeInfo;
USE ExchangeInfo;

CREATE TABLE Exchange (
    ExchangeName VARCHAR(255),
    Address VARCHAR(255),
    TradingHours VARCHAR(255),
    TimeZone VARCHAR(100),
    HasPhysicalTradingFloor BOOLEAN
);

CREATE TABLE Product (
    Symbol VARCHAR(20),
    Contract_Type VARCHAR(50),
    Product_Name VARCHAR(255),
    Asset_Class_Id INT,
    ExchangeId INT,
    PRIMARY KEY (Symbol, Asset_Class_Id, ExchangeId)
);

CREATE TABLE ExchangeInfo.Holiday (
    Holiday_Id INT,
    Holiday_Name VARCHAR(255),
    Is_Early_Close bool,
    Date DATE,
    Calendar_Year INT
);

CREATE TABLE ExchangeInfo.Is_Observed_By (
    Holiday_Id INT,
    Exchange_Id INT
);

INSERT INTO ExchangeInfo.Holiday(Holiday_Id, Holiday_Name, Is_Early_Close, Holiday_Date, Calendar_Year)
VALUES
	(1, "New Year's Day", False, "2025-01-01", 2025),
	(2, "National Day of Mourning - Jimmy Carter", False, "2025-01-09", 2025),
	(3, "Martin Luther King Jr. Day", False, "2025-01-20", 2025),
	(4, "Presidents' Day", False, "2025-02-17", 2025),
	(5, "Good Friday", False, "2025-04-18", 2025),
	(6, "Memorial Day", False, "2025-05-26", 2025),
	(7, "Juneteenth Holiday", False, "2025-06-19", 2025),
	(8, "Independence Day Early Close", True, "2025-07-03", 2025),
	(9, "Independence Day", False, "2025-07-04", 2025),
	(10, "Labor Day", False, "2025-09-01", 2025),
	(11, "Thanksgiving Day", False, "2025-11-27", 2025),
	(12, "Thanksgiving Early Close", True, "2025-11-28", 2025),
	(13, "Christmas Early Close", True, "2025-12-24", 2025),
	(14, "Christmas Day", False, "2025-12-25", 2025);


SELECT * FROM Product
WHERE Contract_Type = "Future"
LIMIT 10

SELECT * FROM Product
WHERE Contract_Type = "Option"
LIMIT 10


SELECT * FROM Product
LIMIT 10

SELECT * FROM Exchange
LIMIT 10

SELECT * FROM AssetClass
LIMIT 10
