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

-- Table: Regulators
CREATE TABLE ExchangeInfo.Regulators (
    Regulator_ID INT PRIMARY KEY,
    Regulator_Name VARCHAR(255),
    Regulator_Type VARCHAR(100),
    Address VARCHAR(255),
    Contact_Information_Website VARCHAR(255),
    Contact_Information_Phone_Number VARCHAR(20)
);

-- Insert data into Regulators
INSERT INTO ExchangeInfo.Regulators VALUES
(1, 'U.S. Securities and Exchange Commission (SEC)', 'Federal Agency', '100 F Street NE, Washington, DC 20549', 'https://www.sec.gov', '202-551-6551'),
(2, 'Commodity Futures Trading Commission (CFTC)', 'Federal Agency', '1155 21st Street NW, Washington, DC 20581', 'https://www.cftc.gov', '202-418-5000'),
(3, 'Financial Industry Regulatory Authority (FINRA)', 'Self-Regulatory Organization', '1735 K Street NW, Washington, DC 20006', 'https://www.finra.org', '301-590-6500'),
(4, 'National Futures Association (NFA)', 'Self-Regulatory Organization', '300 S. Riverside Plaza, Suite 1800, Chicago, IL 60606', 'https://www.nfa.futures.org', '312-781-1300'),
(5, 'Municipal Securities Rulemaking Board (MSRB)', 'Self-Regulatory Organization', '1300 I Street NW, Suite 1000, Washington, DC 20005', 'https://www.msrb.org', '202-838-1500');

-- Table: Is_Supervised_By with COMPOSITE PRIMARY KEY
CREATE TABLE ExchangeInfo.Is_Supervised_By (
    Exchange_ID INT,
    Regulator_ID INT,
    PRIMARY KEY (Exchange_ID, Regulator_ID),
    FOREIGN KEY (Exchange_ID) REFERENCES Exchanges(Exchange_ID),
    FOREIGN KEY (Regulator_ID) REFERENCES Regulators(Regulator_ID)
);

-- Insert relationships
INSERT INTO ExchangeInfo.Is_Supervised_By VALUES
(0, 1),  -- NYSE - SEC
(0, 3),  -- NYSE - FINRA
(1, 1),  -- NASDAQ - SEC
(1, 3),  -- NASDAQ - FINRA
(2, 1),  -- CBOE - SEC
(2, 2),  -- CBOE - CFTC
(2, 3),  -- CBOE - FINRA
(3, 1),  -- CBOE BZX - SEC
(3, 3),  -- CBOE BZX - FINRA
(4, 1),  -- CBOE BYX - SEC
(4, 3),  -- CBOE BYX - FINRA
(5, 1),  -- CBOE EDGA - SEC
(5, 3),  -- CBOE EDGA - FINRA
(6, 1),  -- CBOE EDGX - SEC
(6, 3),  -- CBOE EDGX - FINRA
(7, 1),  -- CBOE C2 - SEC
(7, 3),  -- CBOE C2 - FINRA
(8, 1),  -- IEX - SEC
(8, 3),  -- IEX - FINRA
(9, 1),  -- MIAX - SEC
(9, 3),  -- MIAX - FINRA
(10, 2), -- CME - CFTC
(10, 4); -- CME - NFA


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
