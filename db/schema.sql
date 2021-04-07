CREATE DATABASE IF NOT EXISTS gonk_bot;

use gonk_bot;

DROP TABLE IF EXISTS watch_cog;
CREATE TABLE IF NOT EXISTS watch_cog(
       id INT PRIMARY KEY AUTO_INCREMENT,
       symbol VARCHAR(20),
       user   BIGINT(8),
       status INT DEFAULT 0,
       lower  DOUBLE DEFAULT NULL,
       upper  DOUBLE DEFAULT NULL
);
