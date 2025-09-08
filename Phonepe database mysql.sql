

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

#8 show_transaction_by_state_year

SELECT States, Years, SUM(Transaction_amount) AS Total_Amount
FROM agg_transaction
GROUP BY States, Years
ORDER BY States, Years
LIMIT 100;

#9 show_underutilized_devices_by_state()
USE phonepe;
SELECT States, Device_brand,
           SUM(RegisteredUsers) AS Total_Registered,
           SUM(AppOpens) AS Total_AppOpens,
           ROUND(SUM(AppOpens) / NULLIF(SUM(RegisteredUsers), 0), 2) AS OpenRate
FROM agg_user
GROUP BY States, Device_brand
HAVING SUM(RegisteredUsers) > 10000 AND OpenRate < 0.3
ORDER BY States, OpenRate ASC;

#10 show_state_volatility_summary
WITH joined AS (
        SELECT curr.States, curr.Device_brand,
               curr.User_count - prev.User_count AS UserCount_Change,
               curr.AppOpens - prev.AppOpens AS AppOpens_Change,
               curr.Usage_percentage - prev.Usage_percentage AS UsageChange
        FROM agg_user AS curr
        JOIN agg_user AS prev ON curr.States = prev.States
            AND curr.Device_brand = prev.Device_brand
            AND curr.Years = prev.Years
            AND curr.Quarter = prev.Quarter + 1
    )
    SELECT States,
           ROUND(AVG(UserCount_Change), 2) AS Avg_UserCount_Change,
           ROUND(AVG(AppOpens_Change), 2) AS Avg_AppOpens_Change,
           ROUND(AVG(UsageChange), 2) AS Avg_UsageChange
    FROM joined
    GROUP BY States
    ORDER BY Avg_UsageChange ASC;
    
#11 show_engagement_by_state()
SELECT States,
           SUM(RegisteredUsers) AS Total_Users,
           SUM(AppOpens) AS Total_AppOpens,
           ROUND(SUM(AppOpens) / NULLIF(SUM(RegisteredUsers), 0), 2) AS EngagementRate
    FROM map_user
    GROUP BY States
    ORDER BY EngagementRate DESC;    
    
#12show_conversion_funnel
USE phonepe;
SELECT 
  a.States,
  a.Quarter,
  SUM(a.Transaction_count) AS InsuranceTxns,
  SUM(u.RegisteredUsers) AS RegisteredUsers,
  SUM(u.AppOpens) AS AppOpens,
  ROUND(SUM(u.AppOpens) / NULLIF(SUM(u.RegisteredUsers), 0), 2) AS EngagementRate
FROM agg_insurance a
JOIN agg_user u ON a.States = u.States AND a.Quarter = u.Quarter
GROUP BY a.States, a.Quarter
ORDER BY a.States, a.Quarter; 

#13 show_policy_type_distribution
SELECT 
  States,
  Transaction_type AS PolicyType,
  SUM(Transaction_count) AS Count
FROM agg_insurance
GROUP BY States, Transaction_type
LIMIT 100;

#14 show_transaction_volatility
SELECT States, Quarter, SUM(Transaction_amount) AS TxnAmount
    FROM agg_trans
    GROUP BY States, Quarter
    LIMIT 100;
    
#15 show_transaction_type_mix    
SELECT States, Transaction_type, SUM(Transaction_amount) AS Amount
    FROM agg_trans
    GROUP BY States, Transaction_type
    LIMIT 100;
    
#16 show_yoy_growth_heatmap
SELECT States, Years, SUM(Transaction_amount) AS TxnAmount
    FROM agg_trans
    GROUP BY States, Years
    LIMIT 100;
    
#17 show_device_brand_treemap
SELECT Device_brand, SUM(User_count) AS TotalUsers
    FROM agg_user
    GROUP BY Device_brand;    
    
#18 show_district_engagement_chord
SELECT District, SUM(RegisteredUsers) AS Users, SUM(AppOpens) AS Opens
    FROM map_user
    GROUP BY District
    LIMIT 100;