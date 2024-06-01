-- 데이터베이스 사용
USE tndb;

-- 테이블 생성
CREATE TABLE articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    url VARCHAR(255) NOT NULL,
    writer VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    source VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;