-- 1. Item Catalog Table
CREATE TABLE catalog_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price VARCHAR(50) NOT NULL,
    quantity VARCHAR(50) NOT NULL,
    likes VARCHAR(50)
);

-- example items
INSERT INTO catalog_items (name, price, likes) VALUES
('Laptop', '$999', 20),
('Smartphone', '$699', 2),
('Headphones', '$199', 15);

-- 2. Staff Table
CREATE TABLE Staff (
    employeeID INT PRIMARY KEY,
    employeeName VARCHAR(100) NOT NULL,
    employeeEmail VARCHAR(100) NOT NULL UNIQUE
);

-- 3. Customer Table
CREATE TABLE Customer (
    customerID INT PRIMARY KEY AUTO_INCREMENT,
    customerFirstName VARCHAR(100) NOT NULL,
    customerLastName VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phoneNumber VARCHAR(15),
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL
);

-- example user
INSERT INTO Customer (customerID, customerFirstName, customerLastName, email, username, password) VALUES
('123', 'Admin', 'User', 'admin@example.com', 'admin', 'admin123');

--messages
CREATE TABLE `messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sender` varchar(45) NOT NULL,
  `contents` varchar(100) NOT NULL,
  `receiver` varchar(45) DEFAULT NULL,
  `reply` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
)
