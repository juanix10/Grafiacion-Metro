create database metro;
use metro;

CREATE TABLE IF NOT EXISTS afluencia(
    id INT AUTO_INCREMENT PRIMARY KEY,
    linea VARCHAR(50),
    estacion VARCHAR(100),
    afluencia BIGINT
);