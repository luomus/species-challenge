-- init_db.sql

CREATE DATABASE IF NOT EXISTS species_challenge_dev;
GRANT ALL PRIVILEGES ON species_challenge_dev.* TO 'sc_user_dev'@'%' IDENTIFIED BY 'sc_password_dev';
FLUSH PRIVILEGES;
