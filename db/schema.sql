CREATE DATABASE IF NOT EXISTS gonk_bot;

use gonk_bot;

CREATE TABLE IF NOT EXISTS watch_cog(
       id int primary key auto_increment,
       user   varchar(20),
       coin   varchar(20),
       status int default 0,
       low    int default 0,
       high   int default 0
);
