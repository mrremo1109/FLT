import sqlite3
from datetime import datetime, timedelta

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
sql = "INSERT INTO flights (origin_city, destination_city, airline, NoofConnection, depart_date, available_seates, price) VALUES (?, ?, ?, ?, ?, ?, ?)"
data = [
    ('Chennai', 'Madurai', 'Indian Airways', 1, datetime.now() + timedelta(1), 100, 120),
    ('Bangalore', 'Madurai', 'Indian Airways', 1, datetime.now() + timedelta(1), 100, 130),
    ('Goa', 'Madurai', 'Indian Airways', 1, datetime.now() + timedelta(1), 100, 100),
    ('Chennai', 'Hyderabad', 'Indian Airways', 1, datetime.now() + timedelta(1), 100, 60),
    ('Bangalore', 'Hyderabad', 'Indian Airways', 1, datetime.now() + timedelta(1), 100, 300),
    ('Goa', 'Hyderabad', 'Indian Airways', 1, datetime.now() + timedelta(1), 100, 40),
    ('Chennai', 'Rameshwaram', 'Indian Airways', 1, datetime.now() + timedelta(1), 100, 50),
    ('Bangalore', 'Rameshwaram', 'Indian Airways', 1, datetime.now() + timedelta(1), 100, 300),
    ('Goa', 'Rameshwaram', 'Indian Airways', 1, datetime.now() + timedelta(1), 100, 30),
    ('Chennai', 'Madurai', 'Emirates', 2, datetime.now() + timedelta(1), 100, 200),
    ('Bangalore', 'Madurai', 'Emirates', 2, datetime.now() + timedelta(1), 100, 500),
    ('Goa', 'Madurai', 'Emirates', 2, datetime.now() + timedelta(1), 100, 300),
    ('Chennai', 'Hyderabad', 'Emirates', 2, datetime.now() + timedelta(1), 100, 70),
    ('Bangalore', 'Hyderabad', 'Emirates', 2, datetime.now() + timedelta(1), 100, 400),
    ('Goa', 'Hyderabad', 'Emirates', 2, datetime.now() + timedelta(1), 100, 40),
    ('Chennai', 'Rameshwaram', 'Emirates', 2, datetime.now() + timedelta(1), 100, 50),
    ('Bangalore', 'Rameshwaram', 'Emirates', 2, datetime.now() + timedelta(1), 100, 80),
    ('Goa', 'Rameshwaram', 'Emirates', 2, datetime.now() + timedelta(1), 100, 100),
    ('Chennai', 'Madurai', 'Deccan Airways', 1, datetime.now() + timedelta(1), 100, 60),
    ('Bangalore', 'Madurai', 'Deccan Airways', 2, datetime.now() + timedelta(1), 100, 800),
    ('Goa', 'Madurai', 'Deccan Airways', 1, datetime.now() + timedelta(1), 100, 30),
    ('Chennai', 'Hyderabad', 'Deccan Airways', 2, datetime.now() + timedelta(1), 100, 40),
    ('Bangalore', 'Hyderabad', 'Deccan Airways', 1, datetime.now() + timedelta(1), 100, 60),
    ('Goa', 'Hyderabad', 'Deccan Airways', 2, datetime.now() + timedelta(1), 100, 50),
    ('Chennai', 'Rameshwaram', 'Deccan Airways', 1, datetime.now() + timedelta(1), 100, 90),
    ('Bangalore', 'Rameshwaram', 'Deccan Airways', 2, datetime.now() + timedelta(1), 100, 100),
    ('Goa', 'Rameshwaram', 'Deccan Airways', 1, datetime.now() + timedelta(1), 100, 500),
]
for i in data:
    cur.execute(sql,i)

print("Database initialized")

connection.commit()
connection.close()
