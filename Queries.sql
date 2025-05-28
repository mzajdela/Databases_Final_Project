--Number of symbols listed on CME exchange (Products, Exchange) that are a future but not an option
SELECT COUNT(DISTINCT p.Symbol) AS NumFuturesOnlyOnCME
FROM Product p
JOIN Exchange e ON p.ExchangeId = e.ExchangeId
WHERE e.ExchangeName = 'CME'
  AND p.Contract_Type = 'Future'
  AND p.Symbol NOT IN (
      SELECT Symbol
      FROM Product
      WHERE Contract_Type = 'Option'
        AND ExchangeId = e.ExchangeId
  );
--All exchanges that have AAPL listed but don’t have ZBRA listed
SELECT DISTINCT e.ExchangeName
FROM Product p
JOIN Exchange e ON p.ExchangeId = e.ExchangeId
WHERE p.Symbol = 'AAPL'
  AND NOT EXISTS (
      SELECT 1
      FROM Product p2
      WHERE p2.Symbol = 'ZBRA'
        AND p2.ExchangeId = e.ExchangeId
  );

--Unique symbols for each contract type that trade at the CME
SELECT p.Contract_Type, COUNT(DISTINCT p.Symbol) AS UniqueSymbolCount
FROM Product p
JOIN Exchange e ON p.ExchangeId = e.ExchangeId
WHERE e.ExchangeName = 'CME'
GROUP BY p.Contract_Type;

--All exchanges located in either Chicago or New York
SELECT ExchangeName
FROM Exchange
WHERE Address LIKE '%Chicago%'
   OR Address LIKE '%New York%';

--All products that are only listed at one exchange
SELECT COUNT(*) AS num_single_exchange_products
FROM (
    SELECT Symbol
    FROM Product
    GROUP BY Symbol
    HAVING COUNT(*) = 1
) AS single_listings;

--All Exchanges that are supervised by the SEC and have TRIP listed
SELECT 
    e.Exchange_Name,
    r.Regulator_Name,
    p.Symbol AS Listed_Symbol
FROM 
    Product p
JOIN Exchanges e ON p.ExchangeId = e.Exchange_ID
JOIN Is_Supervised_By isb ON e.Exchange_ID = isb.Exchange_ID
JOIN Regulators r ON isb.Regulator_ID = r.Regulator_ID
WHERE 
    r.Regulator_ID = 1
    AND p.Symbol = 'TRIP';

-- Count the number of holidays per exchange with early close between June and September
SELECT e.ExchangeName, COUNT(o.HolidayId) AS HolidayCount
FROM ExchangeInfo.Exchanges AS e
JOIN ExchangeInfo.Is_Observed_By AS o
	ON e.ExchangeId = o.ExchangeId
JOIN ExchangeInfo.Holiday AS h
	ON o.HolidayId = h.HolidayId
WHERE h.Holiday_Date >= '2025-06-01'
AND h.Holiday_Date < '2025-09-01'
AND h.IsEarlyClose = True
GROUP BY e.ExchangeName;

-- Display HolidayName and HolidayDate for any holidays that are contained in the CBOE exchange but not in the CME exchange
SELECT h.HolidayName
FROM ExchangeInfo.Holidays AS h
JOIN Is_Observed_By AS o ON h.HolidayId = o.HolidayId
JOIN Exchanges AS e ON e.ExchangeId = o.ExchangeId
WHERE e.ExchangeName = 'CBOE'
AND h.HolidayName NOT IN
	(
	SELECT h.HolidayName, h.HolidayDate
	FROM ExchangeInfo.Holidays AS h
	JOIN Is_Observed_By AS o ON h.HolidayId = o.HolidayId
	JOIN Exchanges AS e ON e.ExchangeId = o.ExchangeId
	WHERE e.ExchangeName = 'CME'
	);


-- Which non DPM Broker Dealers are members of NYSE but not NASDAQ
SELECT b.CIK, CompanyName
FROM Broker_Dealer as b
INNER JOIN Is_A_Member_Of as m
	on b.CIK = m.CIK
WHERE Is_DPM = 0
	AND ExchangeId = 1
	AND	b.CIK NOT IN (
		SELECT b.CIK
		FROM Broker_Dealer as b
		INNER JOIN Is_A_Member_Of as m
			on b.CIK = m.CIK
		WHERE Is_DPM = 0
			AND ExchangeId = 2
);

-- Find DPMs who only have 10 Full Holidays (not early close) they Celebrate
SELECT  b.CompanyName, b.CompanyAddress, COUNT(DISTINCT h.HolidayId) as Num_Full_Holidays
FROM Is_A_Member_Of as m
INNER JOIN Broker_Dealer as b
	on m.CIK = b.CIK
INNER JOIN Is_Observed_By as o
	on m.ExchangeId = o.ExchangeId
INNER JOIN Holidays as h
	on o.HolidayId = h.HolidayId
WHERE h.IsEarlyClose = False
	AND m.Is_DPM = 1
GROUP BY b.CompanyName, b.CompanyAddress
HAVING Num_Full_Holidays = 10;