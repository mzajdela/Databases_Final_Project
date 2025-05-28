DROP DATABASE IF EXISTS ExchangeInfo;
CREATE DATABASE ExchangeInfo;
USE ExchangeInfo;

-- Table: Exchange
CREATE TABLE Exchange (
    ExchangeId INT AUTO_INCREMENT PRIMARY KEY
    ExchangeName VARCHAR(255),
    Address VARCHAR(255),
    TradingHours VARCHAR(255),
    TimeZone VARCHAR(100),
    HasPhysicalTradingFloor BOOLEAN
);

-- Table: AssetClass
CREATE TABLE AssetClass (
    AssetClassId INT AUTO_INCREMENT PRIMARY KEY,
    AssetClassName VARCHAR(255)
);

CREATE TABLE Product (
    Symbol VARCHAR(20),
    Contract_Type VARCHAR(50),
    Product_Name VARCHAR(255),
    Asset_Class_Id INT,
    ExchangeId INT,
    PRIMARY KEY (Symbol, Asset_Class_Id, ExchangeId)
);

-- Table: Holidays
CREATE TABLE Holidays (
    HolidayId INT,
    HolidayName VARCHAR(255),
    IsEarlyClose bool,
    HolidayDate DATE,
    CalendarYear INT
);

-- Insert data into Holidays
INSERT INTO Holidays(HolidayId, HolidayName, IsEarlyClose, HolidayDate, CalendarYear)
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

-- Table: Is_Observed_By
CREATE TABLE Is_Observed_By (
    HolidayId INT,
    ExchangeId INT
);

-- Insert Data into Is_Observed_By
INSERT INTO Is_Observed_By(HolidayId, ExchangeId)
VALUES
	(1, 0),  -- NYSE
	(3, 0),
	(4, 0),
	(5, 0),
	(6, 0),
	(7, 0),
	(8, 0),
	(9, 0),
	(10, 0),
	(11, 0),
	(12, 0),
	(13, 0),
	(14, 0),
	(1, 1),  -- NASDAQ
	(3, 1),
	(4, 1),
	(5, 1),
	(6, 1),
	(7, 1),
	(8, 1),
	(9, 1),
	(10, 1),
	(11, 1),
	(12, 1),
	(13, 1),
	(14, 1),
	(1, 2),  -- CBOE BZX
	(2, 2),
	(3, 2),
	(4, 2),
	(5, 2),
	(6, 2),
	(7, 2),
	(8, 2),
	(9, 2),
	(10, 2),
	(11, 2),
	(12, 2),
	(13, 2),
	(14, 2),
	(1, 3),  -- CBOE BYX
	(2, 3),
	(3, 3),
	(4, 3),
	(5, 3),
	(6, 3),
	(7, 3),
	(8, 3),
	(9, 3),
	(10, 3),
	(11, 3),
	(12, 3),
	(13, 3),
	(14, 3),
	(1, 4),  -- CBOE EDGA
	(2, 4),
	(3, 4),
	(4, 4),
	(5, 4),
	(6, 4),
	(7, 4),
	(8, 4),
	(9, 4),
	(10, 4),
	(11, 4),
	(12, 4),
	(13, 4),
	(14, 4),
	(1, 5),  -- CBOE EDGX
	(2, 5),
	(3, 5),
	(4, 5),
	(5, 5),
	(6, 5),
	(7, 5),
	(8, 5),
	(9, 5),
	(10, 5),
	(11, 5),
	(12, 5),
	(13, 5),
	(14, 5),
	(1, 6),  -- CBOE C2
	(2, 6),
	(3, 6),
	(4, 6),
	(5, 6),
	(6, 6),
	(7, 6),
	(8, 6),
	(9, 6),
	(10, 6),
	(11, 6),
	(12, 6),
	(13, 6),
	(14, 6),
	(1, 7),  -- CBOE
	(2, 7),
	(3, 7),
	(4, 7),
	(5, 7),
	(6, 7),
	(7, 7),
	(8, 7),
	(9, 7),
	(10, 7),
	(11, 7),
	(12, 7),
	(13, 7),
	(14, 7),
	(1, 8),  -- IEX
	(3, 8),
	(4, 8),
	(5, 8),
	(6, 8),
	(7, 8),
	(8, 8),
	(9, 8),
	(10, 8),
	(11, 8),
	(12, 8),
	(13, 8),
	(14, 8),
	(1, 9),  -- MIAX
	(3, 9),
	(4, 9),
	(5, 9),
	(6, 9),
	(7, 9),
	(8, 9),
	(9, 9),
	(10, 9),
	(11, 9),
	(12, 9),
	(13, 9),
	(14, 9),
	(1, 10),  -- CME
	(3, 10),
	(4, 10),
	(5, 10),
	(6, 10),
	(7, 10),
	(8, 10),
	(9, 10),
	(10, 10),
	(11, 10),
	(12, 10),
	(13, 10),
	(14, 10);

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

CREATE TABLE Broker_Dealer(
	CIK		INTEGER		NOT NULL,
    	CompanyName	VARCHAR(50)	DEFAULT 'unknown name',
    	CompanyAddress	VARCHAR(50)	DEFAULT 'unknown location',
    	CHECK (CIK >= 0),
    	PRIMARY KEY(CIK)
);

CREATE TABLE Is_A_Member_Of(
	CIK		INTEGER		NOT NULL,
    	ExchangeId	INTEGER		NOT NULL,
	FOREIGN KEY(CIK) 
		REFERENCES Broker_Dealer(CIK)
		ON DELETE CASCADE,
    	FOREIGN KEY(ExchangeId) 
		REFERENCES Exchange(ExchangeId)
        	ON DELETE CASCADE
);


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
