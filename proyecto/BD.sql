create database metro;
use metro;

CREATE TABLE Delegacion (
    id_delegacion INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    poblacion INT,
    area FLOAT
);

CREATE TABLE Estacion (
    id_estacion INT AUTO_INCREMENT PRIMARY KEY,
    nombre_estacion VARCHAR(255) NOT NULL,
    id_delegacion INT,
    linea VARCHAR(50),
    FOREIGN KEY (id_delegacion) REFERENCES Delegacion(id_delegacion)
);

CREATE TABLE Afluencia (
    id_afluencia INT AUTO_INCREMENT PRIMARY KEY,
    id_estacion INT,
    fecha DATE NOT NULL,
    cantidad_usuarios INT NOT NULL,
    FOREIGN KEY (id_estacion) REFERENCES Estacion(id_estacion)
);

CREATE TABLE Usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    rol VARCHAR(50)
);
