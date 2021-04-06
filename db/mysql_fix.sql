-- First login to MySQL as sudo user, then execute the SQL commands
-- sudo mysql -u root

SELECT User,Host FROM mysql.user;
DROP USER 'root'@'localhost';

CREATE USER 'root'@'%' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

EXIT

-- Now login as a non-sudo user :)
