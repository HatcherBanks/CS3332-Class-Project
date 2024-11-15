-- 1. Item Catalog Table
CREATE TABLE ItemCatalog (
    itemID INT PRIMARY KEY,
    itemName VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT
);

-- 2. Staff Table
CREATE TABLE Staff (
    employeeID INT PRIMARY KEY,
    employeeName VARCHAR(100) NOT NULL,
    employeeEmail VARCHAR(100) NOT NULL UNIQUE
);

-- 3. Customer Table
CREATE TABLE Customer (
    customerID INT PRIMARY KEY,
    customerName VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phoneNumber VARCHAR(15)
);
