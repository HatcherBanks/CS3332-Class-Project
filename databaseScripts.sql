-- 1. Item Catalog Table
CREATE TABLE catalog_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price VARCHAR(50) NOT NULL
);

-- example items
INSERT INTO catalog_items (name, price) VALUES
('Laptop', '$999'),
('Smartphone', '$699'),
('Headphones', '$199');

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