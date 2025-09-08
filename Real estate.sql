SELECT * FROM realestate.real_estate;

SELECT COUNT(*) AS Total_Properties
FROM real_estate;

SELECT 
  Booking_Flag AS Booking_Status,
  COUNT(*) AS Property_Count
FROM real_estate
GROUP BY Booking_Flag;

SELECT 
  Builder,
  ROUND(AVG(Ticket_Price_Cr), 2) AS Avg_Ticket_Price_Cr
FROM real_estate
GROUP BY Builder
ORDER BY Avg_Ticket_Price_Cr DESC;

SELECT host FROM mysql.user WHERE user = 'root';

ALTER USER 'powerbi'@'localhost' IDENTIFIED WITH mysql_native_password BY 'YourSecurePassword';
FLUSH PRIVILEGES;

DROP USER 'powerbi'@'localhost';
CREATE USER 'powerbi'@'localhost' IDENTIFIED WITH mysql_native_password BY 'YourSecurePassword';
GRANT ALL PRIVILEGES ON realestate.* TO 'powerbi'@'localhost';
FLUSH PRIVILEGES;

SHOW GRANTS FOR 'powerbi'@'localhost';

SHOW DATABASES;

GRANT ALL PRIVILEGES ON realestate.* TO 'powerbi'@'localhost';
FLUSH PRIVILEGES;

SELECT user, plugin FROM mysql.user WHERE user = 'root';

ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Harshaaa@123';
FLUSH PRIVILEGES;

ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Harshaaa@123';
FLUSH PRIVILEGES;
SET PERSIST mysqlx_enable_hello_notice = OFF;

CREATE USER 'bi_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'BIuser@123';
GRANT SELECT ON realestate.* TO 'bi_user'@'localhost';
FLUSH PRIVILEGES;

GRANT SELECT ON realestate.* TO 'ali'@'localhost';
FLUSH PRIVILEGES;
