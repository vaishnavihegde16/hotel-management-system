import mysql.connector as connector
from datetime import datetime, timedelta

global con, cur
con = connector.connect(host='localhost', port='3306', user='root', password='root', database='hoteldatabasem')
cur = con.cursor()

def create_tables():
    queries = [
        "CREATE TABLE IF NOT EXISTS customerdetails (cid INT PRIMARY KEY, aadhar CHAR(20), cname CHAR(50), cage INT, phone CHAR(20), caddress CHAR(100), finalprice FLOAT, checkin DATE, checkout DATE)",
        "CREATE TABLE IF NOT EXISTS room (roomnum INT PRIMARY KEY, roomtypeid INT, size INT)",
        "CREATE TABLE IF NOT EXISTS roomtype (roomtypeid INT PRIMARY KEY, bednum INT, ac CHAR(10), rate FLOAT, description CHAR(200))",
        "CREATE TABLE IF NOT EXISTS roomservice (orderid INT PRIMARY KEY, itemid INT, quantity INT, rscid INT)",
        "CREATE TABLE IF NOT EXISTS items (itemid INT PRIMARY KEY, itemname CHAR(20), rate FLOAT)",
        "CREATE TABLE IF NOT EXISTS bookingdetails (bid INT PRIMARY KEY, cid INT, checkin DATE, checkout DATE, finalprice FLOAT)",
        "CREATE TABLE IF NOT EXISTS employees (empid INT PRIMARY KEY, aadhar CHAR(20), ename CHAR(50), age INT, gender CHAR(10), roleid INT, sal FLOAT)",
        "CREATE TABLE IF NOT EXISTS roles (roleid INT PRIMARY KEY, rolename CHAR(50), sal FLOAT)"
        "CREATE TABLE IF NOT EXISTS customer_employee_join (aadhar CHAR(20) UNIQUE, cname CHAR(50))"
    ]
    
    for query in queries:
        cur.execute(query)

def add_default_values():
    queries = [
        "INSERT INTO customerdetails VALUES (115, '669524138972', 'Rohit M S', 20, '9358432100', '#41, 1st Main, Marathahalli, Bangalore', 1500, '2022-11-12', '2022-11-13')",
        "INSERT INTO roles VALUES (11, 'Manager', 95000)",
        "INSERT INTO employees VALUES (31, '668574239817', 'Samuel Johnson', 32, 'Male', 11, 95000)",
        "INSERT INTO items VALUES (1, 'Chocolate Ice Cream', 150)",
        "INSERT INTO roomtype VALUES (1, 2, 'AC', 2500, 'Comfortable double room with AC, two single beds, a wardrobe and an outward facing window')",
        "INSERT INTO room VALUES (188, 1, 268)",
        "INSERT INTO roomservice VALUES (1768, 1, 3, 115)",
        "INSERT INTO bookingdetails VALUES (1327, 115, '2022-11-12', '2022-11-13', 1950)"
    ]
    for query in queries:
        cur.execute(query)
        con.commit()

def add_foreign_keys():
    queries = [
        "ALTER TABLE room ADD FOREIGN KEY(roomtypeid) REFERENCES roomtype(roomtypeid) ON UPDATE CASCADE ON DELETE CASCADE",
        "ALTER TABLE roomservice ADD FOREIGN KEY(itemid) REFERENCES items(itemid) ON UPDATE CASCADE ON DELETE CASCADE",
        "ALTER TABLE bookingdetails ADD FOREIGN KEY(cid) REFERENCES customerdetails(cid) ON UPDATE CASCADE ON DELETE CASCADE",
        "ALTER TABLE employees ADD FOREIGN KEY(roleid) REFERENCES roles(roleid) ON UPDATE CASCADE ON DELETE CASCADE",
        "ALTER TABLE roomservice ADD FOREIGN KEY(rscid) REFERENCES customerdetails(cid)"
        "ALTER TABLE customer_employee_join ADD FOREIGN KEY(aadhar) REFERENCES customerdetails(aadhar) ON UPDATE CASCADE ON DELETE CASCADE"
    ]
    for query in queries:
        cur.execute(query)
        con.commit()

def addCustDetails(aadhar, cname, cage, phone, caddress, finalprice, checkin, checkout):
    query = 'SELECT MAX(cid) FROM customerdetails'
    cur.execute(query)
    row = cur.fetchone()
    cid = row[0] + 10 if row[0] else 10

    query = f"INSERT INTO customerdetails VALUES ({cid}, '{aadhar}', '{cname}', {cage}, '{phone}', '{caddress}', {finalprice}, '{checkin}', '{checkout}')"
    cur.execute(query)
    con.commit()
    return cid

def addEmployeeDetails(empid, aadhar, ename, age, gender, roleid):
    query = f'SELECT sal FROM roles WHERE roleid = {roleid}'
    cur.execute(query)
    result = cur.fetchone()

    if result is not None:
        sal = result[0]

        query = f"INSERT INTO employees VALUES ({empid}, '{aadhar}', '{ename}', {age}, '{gender}', {roleid}, {sal})"
        cur.execute(query)
        con.commit()
    else:
        print(f"Role with roleid {roleid} not found.")








# Similar functions for adding items, roles, room types, room service, room, and booking details
def addItem(itemid, itemname, itemrate):
    query = f"INSERT INTO items VALUES ({itemid}, '{itemname}', {itemrate})"
    cur.execute(query)
    con.commit()

#def addCustomerEmployeeDetails(aadhar, cname):
    #query = f"INSERT INTO customer_employee_join VALUES ('{aadhar}', '{cname}')"
   # cur.execute(query)
  #  con.commit()


def addRole(roleid, rolename, rolesal):
    query = f"INSERT INTO roles VALUES ({roleid}, '{rolename}', {rolesal})"
    cur.execute(query)
    con.commit()

def addRoomType(roomtypeid, bednum, ac, roomrate, desc):
    query = f"INSERT INTO roomtype VALUES ({roomtypeid}, {bednum}, '{ac}', {roomrate}, '{desc}')"
    cur.execute(query)
    con.commit()

def addRoomService(itemid, quantity, rscid):
    query = 'SELECT MAX(orderid) FROM roomservice'
    cur.execute(query)
    result = cur.fetchone()
    
    if result:
        orderid = result[0] + 10
    else:
        orderid = 10

    query = f"INSERT INTO roomservice VALUES ({orderid}, {itemid}, {quantity}, {rscid})"
    cur.execute(query)
    con.commit()



def addRoom(roomnum, roomid, size):
    query = f"INSERT INTO room VALUES ({roomnum}, {roomid}, {size})"
    cur.execute(query)
    con.commit()

def addBookingDetails(cid, totalamt):
    query = 'SELECT MAX(bid) FROM bookingdetails'
    cur.execute(query)
    bid = cur.fetchone()[0] + 10 if cur.fetchone()[0] else 10

    query = f"INSERT INTO bookingdetails VALUES ({bid}, {cid}, CURRENT_DATE, CURRENT_DATE + INTERVAL 1 DAY, {totalamt})"
    cur.execute(query)
    con.commit()


def selectRoom(roomtypeid, checkin, checkout):
    query = f'SELECT rate FROM roomtype WHERE roomtypeid = {roomtypeid}'
    cur.execute(query)
    row = cur.fetchone()
    
    if row:
        rate = int(row[0])
        delta = checkout - checkin
        totalprice = rate * delta.days
        return totalprice
    else:
        return 0

# Similar functions for getting customer details, room type, items, roles, employees, rooms, booking details, and orders
def getCustDetails(cid):
    query = f'SELECT * FROM customerdetails WHERE cid = {cid}'
    cur.execute(query)
    row = cur.fetchone()
    return row

def getRoomType(roomtypeid):
    query = f'SELECT * FROM roomtype WHERE roomtypeid = {roomtypeid}'
    cur.execute(query)
    row = cur.fetchone()
    return row

def getCustomerEmployeeDetailsByAadhar(aadhar):
    query = f"SELECT * FROM customer_employee_join WHERE aadhar = '{aadhar}'"
    cur.execute(query)
    rows = cur.fetchone()
    return rows


def getAllItems():
    query = 'SELECT * FROM items'
    cur.execute(query)
    rows = cur.fetchall()
    return rows

def getAllRoles():
    query = 'SELECT * FROM roles'
    cur.execute(query)
    rows = cur.fetchall()
    return rows

def getAllEmployees():
    query = 'SELECT * FROM employees'
    cur.execute(query)
    rows = cur.fetchall()
    return rows

def getAllRooms():
    query = 'SELECT * FROM room'
    cur.execute(query)
    rows = cur.fetchall()
    return rows

def getAllRoomTypes():
    query = 'SELECT * FROM roomtype'
    cur.execute(query)
    rows = cur.fetchall()
    return rows

def getAllBookingDetails():
    query = 'SELECT * FROM bookingdetails'
    cur.execute(query)
    rows = cur.fetchall()
    return rows

def getAllCustomerDetails():
    query = 'SELECT * FROM customerdetails'
    cur.execute(query)
    rows = cur.fetchall()
    return rows

def getAllOrders():
    query = 'SELECT * FROM roomservice'
    cur.execute(query)
    rows = cur.fetchall()
    return rows


# Main functions for getting all records

# ... (previous code)

def getFinalAmount(cid):
    query1 = f"SELECT finalprice FROM customerdetails WHERE cid = {cid}"
    cur.execute(query1)
    row1 = cur.fetchone()
    p1 = float(row1[0]) if row1 else 0

    query2 = f"SELECT SUM(items.rate * roomservice.quantity) AS total_price FROM roomservice JOIN items ON roomservice.itemid = items.itemid WHERE roomservice.rscid = {cid}"
    cur.execute(query2)
    row2 = cur.fetchone()

    try:
        p2 = float(row2[0]) if row2 else 0
    except TypeError:
        p2 = 0

    return p1 + p2


