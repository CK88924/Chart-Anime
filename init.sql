CREATE DATABASE IF NOT EXISTS `CHART`;
USE `CHART`;

CREATE TABLE IF NOT EXISTS `CHART`.`products` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL UNIQUE,
    product_quantity INT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT IGNORE INTO products (product_name, product_quantity) VALUES
('襯衫', 5),
('羊毛衫', 50),
('雪紡', 100),
('褲子', 90),
('鞋子', 110),
('襪子', 30);
