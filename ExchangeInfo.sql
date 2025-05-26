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
    PRIMARY KEY (Symbol, Asset_Class_Id)
);




SELECT * FROM Product
WHERE Contract_Type = "Future"
LIMIT 10

SELECT * FROM Product
WHERE Contract_Type = "Option"
LIMIT 10

SELECT * FROM Exchange
LIMIT 10
