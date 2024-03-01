import sqlite3
import json
from datetime import datetime, timedelta

# Establish connection to the SQLite database
connection = sqlite3.connect('database.db')

# Create the tables using the schema
with open('schema.sql') as f:
    connection.executescript(f.read())

# Initialize a cursor
cur = connection.cursor()

# Define the SQL statement to insert data into the flights table
sql = "INSERT INTO flights (origin_city, destination_city, airline, NoofConnection, depart_date, available_seates, price, Duration, Layover, BaggageInfo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

# Data to be inserted into the flights table
data = [
    ('CHENNAI', 'MADURAI', 'INDIAN AIRWAYS', 1, datetime.now() + timedelta(1), 100, 120,'2 Hrs', '0', '2-Piece 40 Kgs'),
    ('BANGALORE', 'MADURAI', 'INDIAN AIRWAYS', 1, datetime.now() + timedelta(1), 100, 130,'2 Hrs', '0', '1-Piece 20 Kgs'),
    ('GOA', 'MADURAI', 'INDIAN AIRWAYS', 1, datetime.now() + timedelta(1), 100, 100,'2 Hrs', '0', '2-Piece 40 Kgs'),
    ('CHENNAI', 'HYDERABAD', 'INDIAN AIRWAYS', 1, datetime.now() + timedelta(1), 100, 60,'2 Hrs', '0', '1-Piece 20 Kgs'),
    ('BANGALORE', 'HYDERABAD', 'INDIAN AIRWAYS', 1, datetime.now() + timedelta(1), 100, 300,'2 Hrs', '0', '2-Piece 40 Kgs'),
    ('GOA', 'HYDERABAD', 'INDIAN AIRWAYS', 1, datetime.now() + timedelta(1), 100, 40,'2 Hrs', '0','1-Piece 20 Kgs'),
    ('CHENNAI', 'RAMESHWARAM', 'INDIAN AIRWAYS', 1, datetime.now() + timedelta(1), 100, 50,'2 Hrs', '0', '2-Piece 40 Kgs'),
    ('BANGALORE', 'RAMESHWARAM', 'INDIAN AIRWAYS', 1, datetime.now() + timedelta(1), 100, 300,'2 Hrs', '0','1-Piece 20 Kgs'),
    ('GOA', 'RAMESHWARAM', 'INDIAN AIRWAYS', 1, datetime.now() + timedelta(1), 100, 30,'2 Hrs', '0','2-Piece 40 Kgs'),
    ('CHENNAI', 'MADURAI', 'EMIRATES', 2, datetime.now() + timedelta(1), 100, 200,'4 Hrs', '2 Hrs','1-Piece 20 Kgs'),
    ('BANGALORE', 'MADURAI', 'EMIRATES', 2, datetime.now() + timedelta(1), 100, 500,'5 Hrs', '2.5 Hrs','2-Piece 40 Kgs'),
    ('GOA', 'MADURAI', 'EMIRATES', 2, datetime.now() + timedelta(1), 100, 300,'4.5 Hrs', '1 Hrs','1-Piece 20 Kgs'),
    ('CHENNAI', 'HYDERABAD', 'EMIRATES', 2, datetime.now() + timedelta(1), 100, 70,'3 Hrs', '1.5 Hrs','2-Piece 40 Kgs'),
    ('BANGALORE', 'HYDERABAD', 'EMIRATES', 2, datetime.now() + timedelta(1), 100, 400,'3 Hrs', '1 Hrs','1-Piece 20 Kgs'),
    ('GOA', 'HYDERABAD', 'EMIRATES', 2, datetime.now() + timedelta(1), 100, 40,'2.5 Hrs', '0.5 Hrs','2-Piece 40 Kgs'),
    ('CHENNAI', 'RAMESHWARAM', 'EMIRATES', 2, datetime.now() + timedelta(1), 100, 50,'3.5 Hrs', '1.5 Hrs','1-Piece 20 Kgs'),
    ('BANGALORE', 'RAMESHWARAM', 'EMIRATES', 2, datetime.now() + timedelta(1), 100, 80,'4.5 Hrs', '2 Hrs','2-Piece 40 Kgs'),
    ('GOA', 'RAMESHWARAM', 'EMIRATES', 2, datetime.now() + timedelta(1), 100, 100,'4.5 Hrs', '2 Hrs','1-Piece 20 Kgs'),
    ('CHENNAI', 'MADURAI', 'DECCAN AIRWAYS', 1, datetime.now() + timedelta(1), 100, 60,'2 Hrs', '0','2-Piece 40 Kgs'),
    ('BANGALORE', 'MADURAI', 'DECCAN AIRWAYS', 2, datetime.now() + timedelta(1), 100, 800,'3.5 Hrs', '1 Hrs','1-Piece 20 Kgs'),
    ('GOA', 'MADURAI', 'DECCAN AIRWAYS', 1, datetime.now() + timedelta(1), 100, 30,'2 Hrs', '0','2-Piece 40 Kgs'),
    ('CHENNAI', 'HYDERABAD', 'DECCAN AIRWAYS', 2, datetime.now() + timedelta(1), 100, 40,'2.5 Hrs', '1 Hrs','1-Piece 20 Kgs'),
    ('BANGALORE', 'HYDERABAD', 'DECCAN AIRWAYS', 1, datetime.now() + timedelta(1), 100, 60,'2 Hrs', '0','1-Piece 20 Kgs'),
    ('GOA', 'HYDERABAD', 'DECCAN AIRWAYS', 2, datetime.now() + timedelta(1), 100, 50,'3 Hrs', '1.5 Hrs','2-Piece 40 Kgs'),
    ('CHENNAI', 'RAMESHWARAM', 'DECCAN AIRWAYS', 1, datetime.now() + timedelta(1), 100, 90,'2 Hrs', '0','1-Piece 20 Kgs'),
    ('BANGALORE', 'RAMESHWARAM', 'DECCAN AIRWAYS', 2, datetime.now() + timedelta(1), 100, 100,'3.5 Hrs', '0.5 Hrs','2-Piece 40 Kgs'),
    ('GOA', 'RAMESHWARAM', 'DECCAN AIRWAYS', 1, datetime.now() + timedelta(1), 100, 500,'2 Hrs', '0','1-Piece 20 Kgs'),
]

# Insert data into the flights table
for i in data:
    cur.execute(sql, i)

connection.commit()

# Fetch all data from the flights table
cur.execute("SELECT * FROM flights")
flight_data = cur.fetchall()

# Close the database connection
connection.close()

## Convert fetched data to a list of dictionaries
flights_json = []
for flight in flight_data:
    flight_dict = {
        "origin_city": flight[0],
        "destination_city": flight[1],
        "airline": flight[2],
        "NoofConnection": flight[3],
        "depart_date": str(flight[4]),  # Convert datetime object to string
        "available_seates": flight[5],
        "price": flight[6],
        "Duration": flight[7],  # Include Duration in the JSON
        "Layover": flight[8],  # Include Layover in the JSON
        "BaggageInfo": flight[9]  # Include BaggageInfo in the JSON
    }
    flights_json.append(flight_dict)

# Print the flight data in JSON format
print(json.dumps(flights_json, indent=4))

