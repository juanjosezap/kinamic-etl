-- Create database if not exists
CREATE DATABASE IF NOT EXISTS scrapinghub_db;

-- Use the database
USE scrapinghub_db;

-- Create artworks table
CREATE TABLE IF NOT EXISTS artworks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    artist VARCHAR(255),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    image VARCHAR(255),
    categories VARCHAR(255),
    price DECIMAL(10, 2),
    dated VARCHAR(50),
    date_added VARCHAR(50),
    location VARCHAR(50),
    width DECIMAL(10, 2),
    height DECIMAL(10, 2),
    medium VARCHAR(100),
    dimensions VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;