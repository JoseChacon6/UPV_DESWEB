CREATE DATABASE p1_db;
\connect p1_db;

DROP TABLE IF EXISTS equipos_geodesicos CASCADE;
DROP TABLE IF EXISTS rutas_levantamiento CASCADE;
DROP TABLE IF EXISTS zonas_trabajo CASCADE;

CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE zonas_trabajo (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_creacion DATE NOT NULL,
    responsable VARCHAR(100),
    estado VARCHAR(50),
    area DOUBLE PRECISION,
    perimetro DOUBLE PRECISION,
    geom GEOMETRY(POLYGON, 4326) NOT NULL
);

CREATE TABLE rutas_levantamiento (
    id SERIAL PRIMARY KEY,
    codigo_ruta VARCHAR(50) NOT NULL,
    equipo_usado VARCHAR(100),
    operador VARCHAR(100),
    fecha_toma DATE NOT NULL,
    observaciones TEXT,
    longitud DOUBLE PRECISION,
    geom GEOMETRY(LINESTRING, 4326) NOT NULL
);

CREATE TABLE equipos_geodesicos (
    id SERIAL PRIMARY KEY,
    nombre_equipo VARCHAR(100) NOT NULL,
    tipo_equipo VARCHAR(50),
    marca VARCHAR(100),
    modelo VARCHAR(100),
    fecha_toma_datos DATE NOT NULL,
    ficha_tecnica TEXT,
    geom GEOMETRY(POINT, 4326) NOT NULL
);