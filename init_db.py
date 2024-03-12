import sqlite3
import json
from datetime import datetime, timedelta
import random

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

sql = "INSERT INTO flights (flight_id, origin_city, destination_city, airline, NoofConnection, depart_date, available_seates, price, Duration, Layover, BaggageInfo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

def get_dates():
    start_dt = datetime.now()
    end_dt = datetime(2024, start_dt.month, start_dt.day+1, start_dt.hour, 0)
    dt = start_dt + timedelta(seconds = random.randint(0, int((end_dt - start_dt).total_seconds())))
    return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute)

data = [
    (1265, 'NEW JERSEY', 'NEW YORK', 'DELTA AIRLINES', 0, get_dates(), 100, 120,'2 Hrs', '0', '2-Piece 40 Kgs'),
    (2836, 'CALIFORNIA', 'NEW YORK', 'DELTA AIRLINES', 0, get_dates() , 100, 130,'2 Hrs', '0', '1-Piece 20 Kgs'),
    (2347, 'SEATTLE', 'NEW YORK', 'DELTA AIRLINES', 0, get_dates() , 100, 100,'2 Hrs', '0', '2-Piece 40 Kgs'),
    (9735, 'NEW JERSEY', 'LAS VEGAS', 'DELTA AIRLINES', 0, get_dates() , 100, 60,'2 Hrs', '0', '1-Piece 20 Kgs'),
    (3639, 'CALIFORNIA', 'LAS VEGAS', 'DELTA AIRLINES', 0, get_dates() , 100, 300,'2 Hrs', '0', '2-Piece 40 Kgs'),
    (9173, 'SEATTLE', 'LAS VEGAS', 'DELTA AIRLINES', 0, get_dates() , 100, 40,'2 Hrs', '0','1-Piece 20 Kgs'),
    (1826, 'NEW JERSEY', 'DALLAS', 'DELTA AIRLINES', 0, get_dates() , 100, 50,'2 Hrs', '0', '2-Piece 40 Kgs'),
    (2339, 'CALIFORNIA', 'DALLAS', 'DELTA AIRLINES', 0, get_dates() , 100, 300,'2 Hrs', '0','1-Piece 20 Kgs'),
    (9846, 'SEATTLE', 'DALLAS', 'DELTA AIRLINES', 0, get_dates() , 100, 30,'2 Hrs', '0','2-Piece 40 Kgs'),
    (6892, 'NEW JERSEY', 'NEW YORK', 'EMIRATES', 1, get_dates() , 100, 200,'4 Hrs', '2 Hrs','1-Piece 20 Kgs'),
    (9862, 'CALIFORNIA', 'NEW YORK', 'EMIRATES', 1, get_dates() , 100, 500,'5 Hrs', '2.5 Hrs','2-Piece 40 Kgs'),
    (9237, 'SEATTLE', 'NEW YORK', 'EMIRATES', 1, get_dates() , 100, 300,'4.5 Hrs', '1 Hrs','1-Piece 20 Kgs'),
    (1866, 'NEW JERSEY', 'LAS VEGAS', 'EMIRATES', 1, get_dates() , 100, 70,'3 Hrs', '1.5 Hrs','2-Piece 40 Kgs'),
    (9242, 'CALIFORNIA', 'LAS VEGAS', 'EMIRATES', 1, get_dates() , 100, 400,'3 Hrs', '1 Hrs','1-Piece 20 Kgs'),
    (8636, 'SEATTLE', 'LAS VEGAS', 'EMIRATES', 1, get_dates() , 100, 40,'2.5 Hrs', '0.5 Hrs','2-Piece 40 Kgs'),
    (3223, 'NEW JERSEY', 'DALLAS', 'EMIRATES', 1, get_dates() , 100, 50,'3.5 Hrs', '1.5 Hrs','1-Piece 20 Kgs'),
    (4554, 'CALIFORNIA', 'DALLAS', 'EMIRATES', 1, get_dates() , 100, 80,'4.5 Hrs', '2 Hrs','2-Piece 40 Kgs'),
    (6556, 'SEATTLE', 'DALLAS', 'EMIRATES', 1, get_dates() , 100, 100,'4.5 Hrs', '2 Hrs','1-Piece 20 Kgs'),
    (7667, 'NEW JERSEY', 'NEW YORK', 'UNITED AIRLINES', 0, get_dates() , 100, 60,'2 Hrs', '0','2-Piece 40 Kgs'),
    (8228, 'CALIFORNIA', 'NEW YORK', 'UNITED AIRLINES', 1, get_dates() , 100, 800,'3.5 Hrs', '1 Hrs','1-Piece 20 Kgs'),
    (9229, 'SEATTLE', 'NEW YORK', 'UNITED AIRLINES', 0, get_dates() , 100, 30,'2 Hrs', '0','2-Piece 40 Kgs'),
    (1109, 'NEW JERSEY', 'LAS VEGAS', 'UNITED AIRLINES', 1, get_dates() , 100, 40,'2.5 Hrs', '1 Hrs','1-Piece 20 Kgs'),
    (9113, 'CALIFORNIA', 'LAS VEGAS', 'UNITED AIRLINES', 0, get_dates() , 100, 60,'2 Hrs', '0','1-Piece 20 Kgs'),
    (1991, 'SEATTLE', 'LAS VEGAS', 'UNITED AIRLINES', 1, get_dates() , 100, 50,'3 Hrs', '1.5 Hrs','2-Piece 40 Kgs'),
    (9119, 'NEW JERSEY', 'DALLAS', 'UNITED AIRLINES', 0, get_dates() , 100, 90,'2 Hrs', '0','1-Piece 20 Kgs'),
    (8445, 'CALIFORNIA', 'DALLAS', 'UNITED AIRLINES', 1, get_dates() , 100, 100,'3.5 Hrs', '0.5 Hrs','2-Piece 40 Kgs'),
    (6352, 'SEATTLE', 'DALLAS', 'UNITED AIRLINES', 0, get_dates() , 100, 500,'2 Hrs', '0','1-Piece 20 Kgs'),
]

for i in data:
    cur.execute(sql, i)

connection.commit()

cur.execute("SELECT * FROM flights")
flight_data = cur.fetchall()

connection.close()

flights_json = []
for flight in flight_data:
    flight_dict = {
        "flight_id": flight[0],
        "origin_city": flight[1],
        "destination_city": flight[2],
        "airline": flight[3],
        "NoofConnection": flight[4],
        "depart_date": str(flight[5]),
        "available_seates": flight[6],
        "price": flight[7],
        "Duration": flight[8],
        "Layover": flight[9], 
        "BaggageInfo": flight[10] 
    }
    flights_json.append(flight_dict)

print(json.dumps(flights_json, indent=4))

print("**********Successfully Database Initialized************")