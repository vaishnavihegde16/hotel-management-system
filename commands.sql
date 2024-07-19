-- Create Database
CREATE DATABASE IF NOT EXISTS hoteldatabasem;
USE hoteldatabasem;

-- Creating Tables
CREATE TABLE IF NOT EXISTS customerdetails(
    cid INT PRIMARY KEY,
    aadhar CHAR(20) UNIQUE,
    cname CHAR(50),
    cage INT,
    phone CHAR(20) UNIQUE,
    caddress CHAR(100),
    finalprice FLOAT,
    checkin DATE,
    checkout DATE
);

CREATE TABLE IF NOT EXISTS room(
    roomnum INT PRIMARY KEY,
    roomtypeid INT,
    size INT
);

CREATE TABLE IF NOT EXISTS roomtype(
    roomtypeid INT PRIMARY KEY,
    bednum INT,
    ac CHAR(10),
    rate FLOAT,
    description CHAR(200)
);

CREATE TABLE IF NOT EXISTS roomservice(
    orderid INT PRIMARY KEY,
    itemid INT,
    quantity INT,
    rscid INT
);

CREATE TABLE IF NOT EXISTS items(
    itemid INT PRIMARY KEY,
    itemname CHAR(20),
    rate FLOAT
);

CREATE TABLE IF NOT EXISTS bookingdetails(
    bid INT PRIMARY KEY,
    cid INT,
    checkin DATE,
    checkout DATE,
    finalprice FLOAT
);

CREATE TABLE IF NOT EXISTS employees(
    empid INT PRIMARY KEY,
    aadhar CHAR(20) UNIQUE,
    ename CHAR(50),
    age INT,
    gender CHAR(10),
    roleid INT,
    sal FLOAT
);

CREATE TABLE IF NOT EXISTS roles(
    roleid INT PRIMARY KEY,
    rolename CHAR(50),
    sal FLOAT
);

-- Additional Tables
CREATE TABLE IF NOT EXISTS employee_log(
    empid INT,
    action CHAR(10),
    timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS booking_log(
    bid INT,
    action CHAR(10),
    timestamp TIMESTAMP
);


-- Inserting Example Values
INSERT INTO customerdetails VALUES
    (115,'44444444444','Rohit ',20,'9358432100','#41, 1st Main, Marathahalli, Bangalore',1500,'2022-11-12','2022-11-13'),
    (116,'123456789012','Alice Johnson',25,'9876543210','#123, 2nd Street, Downtown, City',1800,'2022-11-15','2022-11-17'),
    (117,'987654321234','John Doe',30,'9876543211','#456, 3rd Avenue, Uptown, City',2000,'2022-11-18','2022-11-20'),
    (118,'567890123456','Jane Doe',28,'8765432109','#789, 4th Street, Suburb, City',2200,'2022-11-22','2022-11-25');

INSERT INTO roles VALUES
    (11,'Manager',95000),
    (12,'Receptionist',50000),
    (13,'Cleaning Staff',30000),
    (14,'Chef',70000);

INSERT INTO employees VALUES
    (31,'44444444444','rohit',32,'Male',11,95000),
    (32,'987654321234','Emily Williams',28,'Female',12,50000),
    (33,'123456789876','Michael Smith',35,'Male',13,30000),
    (34,'543210987654','Olivia Davis',30,'Female',14,70000);

INSERT INTO items VALUES
    (1,'Chocolate Ice Cream',150),
    (2,'Coffee',50),
    (3,'Pizza',200),
    (4,'Burger',120);

INSERT INTO roomtype VALUES
    (1,2,'AC',2500,'Comfortable double room with AC, two single beds, a wardrobe and an outward facing window'),
    (2,1,'Non-AC',1500,'Cozy single room with a fan and a small desk'),
    (3,3,'AC Suite',3500,'Luxurious suite with AC, a king-size bed, a separate living area, and city views'),
    (4,2,'Deluxe Room',2800,'Spacious room with AC, a queen-size bed, and a private balcony');

INSERT INTO room VALUES
    (188,1,268),
    (189,2,320),
    (190,3,500),
    (191,4,400);

INSERT INTO roomservice VALUES
    (1768,1,3,115),
    (1769,2,2,116),
    (1770,3,1,117),
    (1771,4,2,118);

INSERT INTO bookingdetails VALUES
    (1327,115,'2022-11-12','2022-11-13',1950),
    (1328,116,'2022-11-15','2022-11-17',2400),
    (1329,117,'2022-11-18','2022-11-20',2800),
    (1330,118,'2022-11-22','2022-11-25',3200);

-- Adding Foreign Keys
ALTER TABLE room ADD FOREIGN KEY(roomtypeid) REFERENCES roomtype(roomtypeid) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE roomservice ADD FOREIGN KEY(itemid) REFERENCES items(itemid) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE bookingdetails ADD FOREIGN KEY(cid) REFERENCES customerdetails(cid) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE employees ADD FOREIGN KEY(roleid) REFERENCES roles(roleid) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE roomservice ADD FOREIGN KEY(rscid) REFERENCES customerdetails(cid);

-- Add this SQL query to perform the join between customerdetails and employees
-- Create a new table to store the result of the join
CREATE TABLE IF NOT EXISTS customer_employee_join (
    aadhar CHAR(20) UNIQUE,
    cname CHAR(50)
);

-- Insert the result of the join into the new table
INSERT INTO customer_employee_join (aadhar, cname)
SELECT customerdetails.aadhar, customerdetails.cname
FROM customerdetails
JOIN employees ON customerdetails.aadhar = employees.aadhar;













-- Create Triggers
DELIMITER //

-- Trigger to update final price in customerdetails
CREATE TRIGGER update_final_price
AFTER INSERT ON bookingdetails
FOR EACH ROW
BEGIN
    UPDATE customerdetails
    SET finalprice = NEW.finalprice
    WHERE cid = NEW.cid;
END;

-- Trigger to update room size when a new room is added
CREATE TRIGGER update_room_size
AFTER INSERT ON room
FOR EACH ROW
BEGIN
    IF NEW.size IS NOT NULL THEN
        UPDATE room
        SET size = NEW.size * 1.2; -- Increase size by 20%
    END IF;
END;








-- Trigger to log employee information when a new employee is added
CREATE TRIGGER log_new_employee
AFTER INSERT ON employees
FOR EACH ROW
BEGIN
    INSERT INTO employee_log(empid, action, timestamp)
    VALUES (NEW.empid, 'INSERT', NOW());
END;

-- Trigger to log booking information when a new booking is made
CREATE TRIGGER log_new_booking
AFTER INSERT ON bookingdetails
FOR EACH ROW
BEGIN
    INSERT INTO booking_log(bid, action, timestamp)
    VALUES (NEW.bid, 'INSERT', NOW());
END;

//

DELIMITER ;
-- Your procedures...

-- Set the delimiter to something else (e.g., $$) before defining functions
DELIMITER $$

-- Nested Functions
CREATE FUNCTION CalculateTotalPrice(quantity INT, rate FLOAT)
RETURNS FLOAT
DETERMINISTIC
BEGIN
    RETURN quantity * rate;
END $$

CREATE FUNCTION CalculateDiscountedPrice(originalPrice FLOAT, discountPercentage FLOAT)
RETURNS FLOAT
DETERMINISTIC
BEGIN
    DECLARE discountedPrice FLOAT;
    SET discountedPrice = originalPrice - (originalPrice * discountPercentage / 100);
    RETURN discountedPrice;
END $$

-- Set the delimiter back to ;
DELIMITER ;
-- Call Functions
-- Replace parameters with actual values as needed
CALL CalculateTotalPrice(2.0, 50.0);

-- Replace parameters with actual values as needed
CALL CalculateDiscountedPrice(3000, 10);

