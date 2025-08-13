SELECT * FROM phonepe.map_transaction;

USE phonepe;
SELECT States, ROUND(AVG(lat), 4) AS Latitude, ROUND(AVG(lon), 4) AS Longitude,
 ROUND(SUM(Transaction_amount), 2) AS Total_Transaction_Value
FROM agg_transaction
GROUP BY States
ORDER BY Total_Transaction_Value DESC;

USE phonepe;
SELECT District, ROUND(SUM(Metric_amount), 2) AS Total_Metric_Value,
lat AS Latitude,
lon AS Longitude
FROM map_transaction
GROUP BY District, lat, lon
ORDER BY Total_Metric_Value DESC
LIMIT 10;

USE phonepe;
SELECT Pincodes, ROUND(SUM(Pin_amount), 2) AS Total_Pincode_Value,
lat AS Latitude,
lon AS Longitude
FROM top_transaction
GROUP BY Pincodes, lat, lon
ORDER BY Total_Pincode_Value DESC
LIMIT 10;

#Business case study
#1. Identify Consistently Growing Regions
USE phonepe;
SELECT States, Transaction_type, COUNT(*) AS Growth_Quarters
FROM agg_trans
WHERE Trend = 'Growth'
GROUP BY States, Transaction_type
HAVING COUNT(*) >= 3;    

#2. Detect Declining or Stagnant Regions
USE phonepe;
SELECT States, Transaction_type, COUNT(*) AS Non_Growth_Quarters
FROM agg_trans
WHERE Trend IN ('Decline', 'Stable')
GROUP BY States, Transaction_type
HAVING COUNT(*) >= 3;
    
#3. Quarter-over-Quarter Volatility
USE phonepe;
WITH joined AS (SELECT curr.States, curr.Device_brand, curr.Years, curr.Quarter,
            curr.User_count - prev.User_count AS UserCount_Change,
            curr.AppOpens - prev.AppOpens AS AppOpens_Change,
            curr.Usage_percentage - prev.Usage_percentage AS UsageChange
FROM agg_user AS curr
JOIN agg_user AS prev ON curr.States = prev.States
            AND curr.Device_brand = prev.Device_brand
            AND curr.Years = prev.Years
            AND curr.Quarter = prev.Quarter + 1)
SELECT States, Device_brand, Years, Quarter,
        ROUND(AVG(UserCount_Change), 2) AS Avg_UserCount_Change,
        ROUND(AVG(AppOpens_Change), 2) AS Avg_AppOpens_Change,
        ROUND(AVG(UsageChange), 2) AS Avg_UsageChange
FROM joined
GROUP BY States, Device_brand, Years, Quarter
ORDER BY States, Device_brand, Years, Quarter
LIMIT 50;
    
#4. Map-Ready Output for Streamlit
USE phonepe;
SELECT States, Years, Quarter, Transaction_type, Transaction_amount,
    Trend, lat, lon
FROM agg_trans
WHERE Years = 2018 AND Quarter = 2;
    
#5. Strategic Summary by State
USE phonepe;
SELECT States,
    COUNT(CASE WHEN Trend = 'Growth' THEN 1 END) AS Growth,
    COUNT(CASE WHEN Trend = 'Decline' THEN 1 END) AS Decline,
    COUNT(CASE WHEN Trend = 'Stable' THEN 1 END) AS Stable,
    COUNT(CASE WHEN Trend = 'No Data' THEN 1 END) AS No_Data
FROM agg_trans
GROUP BY States;    

#6.show_pincode_engagement_map
SELECT m.States, m.Years, m.Quarter, m.RegisteredUsers, m.AppOpens,
        ROUND(m.AppOpens / NULLIF(m.RegisteredUsers, 0), 2) AS Engagement_rate, t.Total_pin_amount,
        ROUND(t.Total_pin_amount / NULLIF(m.RegisteredUsers, 0), 2) AS Spend_per_user, t.lat, t.lon
FROM map_user m
JOIN (SELECT States, Years, Quarter, AVG(lat) AS lat, AVG(lon) AS lon, SUM(Pin_amount) AS Total_pin_amount
	  FROM top_transaction
	  GROUP BY States, Years, Quarter) t ON m.States = t.States AND m.Years = t.Years AND m.Quarter = t.Quarter;    

#7 show_insurance_growth
USE phonepe;
SELECT States, Years, Quarter,
           SUM(Transaction_amount) AS Total
    FROM agg_insurance
    GROUP BY States, Years, Quarter
    ORDER BY States, Years, Quarter;

