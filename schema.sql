DROP TABLE IF EXISTS flights;

CREATE TABLE flights (
    origin_city TEXT NOT NULL,
    destination_city TEXT NOT NULL,
    airline TEXT NOT NULL,
    NoofConnection INTEGER NOT NULL,
    depart_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    available_seates INTEGER NOT NULL,
    price DOUBLE NOT NULL,
    Duration INTEGER NOT NULL,
    Layover INTEGER NOT NULL,
    BaggageInfo INTEGER NOT NULL
);
