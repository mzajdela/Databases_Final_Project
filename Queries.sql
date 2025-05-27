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
SELECT COUNT(o.HolidayId), e.ExchangeId
FROM Exchanges AS e
JOIN Is_Observed_By AS o
	ON e.ExchangeId = o.ExchangeId
JOIN Holiday AS h
	ON o.HolidayId = h.HolidayId
WHERE h.HolidayDate >= '06-01-2025'
AND h.HolidayDate < '09-01-2025'
AND h.Is_Early_Close = True
GROUP BY e.ExchangeId
