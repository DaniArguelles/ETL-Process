CREATE DATABASE Hoteles

CREATE TABLE Hoteles(
Id_Hotel INT,
Nombre VARCHAR(50),
Calificacion INT,
Ubicacion INT,
Limpieza INT,
Servicio INT,
Calidad_Precio INT,
Direccion VARCHAR(200),
Telefono VARCHAR(50)
CONSTRAINT PK_Id_Hotel PRIMARY KEY (Id_Hotel)
)

CREATE TABLE Detalles(
Id_Detalle INT,
Id_Hotel INT,
Promedio_Min INT,
Promedio_Max INT,
Habitaciones INT,
Opiniones INT,
CONSTRAINT PK_Id_Detalle PRIMARY KEY (Id_Detalle),
FOREIGN KEY (Id_Hotel) REFERENCES Hoteles(Id_Hotel)
)

CREATE TABLE Servicio(
Id_Servicio INT,
Servicio VARCHAR(100)
CONSTRAINT PK_Id_Servicio PRIMARY KEY (Id_Servicio)
)

CREATE TABLE Detalle_Extendido(
Id_Detalle INT,
Id_Servicio INT,
FOREIGN KEY (Id_Detalle) REFERENCES Detalles(Id_Detalle),
FOREIGN KEY (Id_Servicio) REFERENCES Servicio(Id_Servicio)
)

CREATE TABLE Autores(
Id_Autor INT,
Autor VARCHAR(50)
CONSTRAINT PK_Id_Autor PRIMARY KEY (Id_Autor)
)


CREATE TABLE Opiniones(
Id_Opinion BIGINT,
Id_Hotel INT,
Id_Autor INT,
Fecha DATE, 
YearDate INT,
MonthDate INT,
Calificacion_Opin INT
CONSTRAINT PK_Id_Opinion PRIMARY KEY (Id_Opinion),
FOREIGN KEY (Id_Hotel) REFERENCES Hoteles(Id_Hotel),
FOREIGN KEY (Id_Autor) REFERENCES Autores(Id_Autor)
)

CREATE TABLE Detalle_Opini(
Id_Opinion BIGINT,
Titulo VARCHAR(1000),
Comentario VARCHAR(1000)
FOREIGN KEY (Id_Opinion) REFERENCES Opiniones(Id_Opinion)
)

SELECT * FROM Hoteles
SELECT * FROM Detalles
SELECT * FROM Servicio
SELECT * FROM Detalle_Extendido
SELECT * FROM Autores
SELECT * FROM Opiniones
SELECT * FROM Detalle_Opini

