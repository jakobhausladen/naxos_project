--@block
CREATE DATABASE naxos_db;

--@block
USE naxos_db;

--@block
CREATE TABLE Album (
    catalogue_no VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    label VARCHAR(255),
    genre VARCHAR(255),
    period VARCHAR(255),
    release_date DATE
);

CREATE TABLE Person (
    id BIGINT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    href VARCHAR(255),
    birth_year YEAR,
    death_year YEAR
);

CREATE TABLE Ensemble (
    id BIGINT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    href VARCHAR(255)
);

CREATE TABLE AlbumRole (
    id INT AUTO_INCREMENT PRIMARY KEY,
    album_catalogue_no VARCHAR(255),
    person_id BIGINT NULL,
    ensemble_id BIGINT NULL,
    role ENUM('composer', 'artist', 'conductor', 'lyricist', 'arranger', 'orchestra', 'choir', 'ensemble') NOT NULL,
    UNIQUE (album_catalogue_no, person_id, ensemble_id, role),
    FOREIGN KEY (album_catalogue_no) REFERENCES Album(catalogue_no),
    FOREIGN KEY (person_id) REFERENCES Person(id),
    FOREIGN KEY (ensemble_id) REFERENCES Ensemble(id),
    CHECK (person_id IS NOT NULL OR ensemble_id IS NOT NULL)
);