from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import pytz 
from flask import redirect, url_for
import json
from flask import jsonify
import sqlite3
from datetime import datetime
import os
print(os.getcwd())
import googlemaps
import requests

app = Flask(__name__)
CORS(app)

def execute_query(sql, params=None):
    with sqlite3.connect("database.db") as conn:
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        if sql.strip().lower().startswith('select'):
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        else:
            conn.commit()
            return cursor.rowcount

app.secret_key = 'QWERTY'

@app.route('/')
def index():
    return render_template('index.html')

currency_rates_cache = {}

currency_rates = {
    "USD": 1.0, "EUR": 0.85, "GBP": 0.73,
    "JPY": 150.09, "IQD": 0.31, "INR": 82.85,
}

@app.route('/currency_rates')
def get_currency_rates():
    return jsonify(currency_rates)


def get_all_flights():
    conn = sqlite3.connect('flights.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flights")
    flights = cursor.fetchall()
    conn.close()
    return flights

"""
@app.route('/api/flights_data')
def get_flights_data():
    flights = get_all_flights()
    # Convert fetched flight data to a list of dictionaries
    flights_data = [{'origin_city': row[0], 'destination_city': row[1], 'depart_date': row[2], 'airline': row[3], 'NoofConnection': row[4], 'Duration': row[5], 'Layover': row[6], 'price': row[7]} for row in flights]
    return jsonify({'flights': flights_data})
"""

@app.route('/api/flights_data', methods=['GET'])
def get_flights_data():
    origin_city = request.args.get('originCity')
    destination_city = request.args.get('destinationCity')
    airline = request.args.get('airline')
    selected_currency = request.args.get('currency', 'USD')
    NoofConnection = request.args.get('NoofConnection')

    query = "SELECT * FROM flights WHERE 1=1"
    query_params = []
    if origin_city:
        query += " AND origin_city = ?"
        query_params.append(origin_city)
    if destination_city:
        query += " AND destination_city = ?"
        query_params.append(destination_city)
    if airline:
        query += " AND airline = ?"
        query_params.append(airline)
    if NoofConnection:
        query += " AND NoofConnection = ?"
        query_params.append(NoofConnection)
    flights_data = execute_query(query, query_params)

    if not flights_data:
        return jsonify({"error": "No flights data found"}), 404
    conversion_rate = currency_rates.get(selected_currency, 1)
    for flight in flights_data:
        flight['converted_price'] = round(flight['price'] * conversion_rate, 2)
        flight['currency'] = selected_currency

    return jsonify({"flights": flights_data})


@app.route('/api/available_seates', methods=['GET'])
def get_available_seates():
    sql = "SELECT available_seates FROM flights"
    flights_data = execute_query(sql)
    
    available_seats_list = [flight['available_seates'] for flight in flights_data]
    
    return jsonify(available_seats=available_seats_list)

@app.route('/api/origincity', methods=['GET'])
def get_Origincity():
    sql = "SELECT DISTINCT origin_city FROM flights"
    origin_data = execute_query(sql)
    origin_details = [row['origin_city'] for row in origin_data]
    return jsonify(origin_details)

@app.route('/api/destinationcity', methods=['GET'])
def get_destinationcity():
    sql = "SELECT DISTINCT destination_city FROM flights"
    destination_data = execute_query(sql)
    destination_details = [row['destination_city'] for row in destination_data]
    return jsonify(destination_details)

@app.route('/api/airline', methods=['GET'])
def get_airline():
    sql = "SELECT DISTINCT airline FROM flights"
    airline_data = execute_query(sql)
    airline_details = [row['airline'] for row in airline_data]
    return jsonify(airline_details)

@app.route('/api/departuredate', methods=['GET'])
def get_departuredate():
    sql = "SELECT DISTINCT depart_date FROM flights"
    departuredate_data = execute_query(sql)
    departuredate_details = [row['depart_date'] for row in departuredate_data]
    return jsonify(departuredate_details)

@app.route('/api/Duration', methods=['GET', 'POST'])
def get_Duration():
    sql = "SELECT Duration FROM flights" 
    Duration_data = execute_query(sql)

    if not Duration_data:
        return jsonify({"error": "No flights data found"}), 404

    durations = []
    for row in Duration_data:
        durations.append({"Duration": row['Duration']})

    return jsonify(durations)

@app.route('/api/flight_id', methods=['GET', 'POST'])
def get_flight_id():
    sql = "SELECT flight_id FROM flights" 
    flight_id_data = execute_query(sql)

    if not flight_id_data:
        return jsonify({"error": "No flights data found"}), 404

    flight_id = []
    for row in flight_id_data:
        flight_id.append({"flight_id": row['flight_id']})

    return jsonify(flight_id)

@app.route('/api/NoofConnection', methods=['GET'])
def get_NoofConnection():
    sql = "SELECT DISTINCT NoofConnection FROM flights"
    NoofConnection_data = execute_query(sql)
    NoofConnection_details = [row['NoofConnection'] for row in NoofConnection_data]
    return jsonify(NoofConnection_details)

@app.route('/api/search', methods=['GET'])
def search_data():
    origin_city = request.args.get('originCity')
    destination_city = request.args.get('destinationCity')
    airline = request.args.get('airline')
    
    if airline:
        sql = "SELECT * FROM flights WHERE origin_city=? AND destination_city=? AND airline=?"
        query_parameters = (origin_city, destination_city, airline)
    else:
        sql = "SELECT * FROM flights WHERE origin_city=? AND destination_city=?"
        query_parameters = (origin_city, destination_city)
    
    flights = execute_query(sql, query_parameters)
    
    app.logger.info(f"Number of flights found: {len(flights)}")
    
    if not flights:
        return jsonify({"error": "No flights found for the provided criteria"}), 404
    
    serialized_flights = []
    for flight in flights:
        serialized_flight = {
            "flight_id":flight["flight_id"],
            "origin_city": flight["origin_city"],
            "destination_city": flight["destination_city"],
            "depart_date": flight["depart_date"],
            "airline": flight["airline"],
            "NoofConnection": flight["NoofConnection"],
            "Duration": flight["Duration"],
            "available_seates": flight["available_seates"],
            "Layover": flight["Layover"],
            "BaggageInfo": flight["BaggageInfo"],
            "price": flight["price"]
        }
        serialized_flights.append(serialized_flight)
    
    return jsonify(serialized_flights)


@app.route('/api/flight_details', methods=['GET'])
def get_flight_details():
    flight_details_data = execute_query("SELECT * FROM flight_details")
    if not flight_details_data:
        return jsonify({"error": "No flight details found"}), 404

    flight_details = [dict(flight) for flight in flight_details_data]

    return jsonify(flight_details)

@app.route('/search')
def search():
        origin_city = request.args.get('originCity')
        destination_city = request.args.get('destinationCity')
        sql = "SELECT * FROM flights WHERE origin_city=? AND destination_city=? AND depart_date>=DATE('now')"
        flights = execute_query(sql, (origin_city, destination_city))

        rates = currency_rates

        return render_template('search.html', flights=flights, rates=rates)

def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

@app.route('/bookingdetails', methods=['POST'])
def bookingdetails():
    if request.method == 'POST':
        session['flight_details'] = request.form.to_dict()
        price_in_selected_currency = request.form.get('priceInSelectedCurrency')
        print("Flight Details:", session['flight_details'])
        
        return render_template('bookingdetails.html')
    return "This route should be accessed via POST method."


GOOGLE_MAPS_API_KEY = 'AIzaSyCHfcbLvLze_Uz57qc1Wl4H1TWQ2E_dv5E'
OPENWEATHER_API_KEY = '9cc7cb0d46d0878a0faa22cecf727c72' 


def get_nearby_attractions(dest_coord, api_key):
    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': dest_coord,
        'radius': '5000',
        'type': 'tourist_attraction',
        'key': api_key
    }
    response = requests.get(endpoint_url, params=params)
    if response.status_code == 200:
        attractions = response.json()['results']
    else:
        attractions = []
    return attractions

def get_timezone_offset(timezone):
    tz = pytz.timezone(timezone)
    now = datetime.now(tz)
    offset_hours = now.utcoffset().total_seconds() // 3600
    offset_minutes = (now.utcoffset().total_seconds() // 60) % 60
    offset_str = f"{int(offset_hours):+03}:{int(offset_minutes):02}"
    return f"GMT{offset_str}, {timezone}"

timezone_offset = get_timezone_offset("America/Los_Angeles")
print(timezone_offset)

def get_weather_info(city_name, openweather_api_key):
    endpoint_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': openweather_api_key,
        'units': 'metric'
    }
    response = requests.get(endpoint_url, params=params)
    if response.status_code == 200:
        weather_info = response.json()
        timezone_offset = pytz.timezone('UTC').utcoffset(datetime.now())
        timezone_offset_hours = timezone_offset.total_seconds() / 3600
        weather_info['timezone'] = f"UTC (GMT{timezone_offset_hours:+.2f})"

        return weather_info
    else:
        return {}

def create_flight_details_table():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS flight_details (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    flight_id INTEGER,
                    name TEXT,
                    email TEXT,
                    seat_id TEXT,
                    origin_city TEXT,
                    destination_city TEXT,
                    airline TEXT,
                    depart_date TEXT,
                    no_of_connections INTEGER,
                    duration TEXT,
                    baggage_info TEXT,
                    price REAL,
                    converted_price REAL,
                    currency_code TEXT 
                )''')
    connection.commit()
    connection.close()
    

@app.route('/bookedticket')
def bookedticket():
    booked_tickets = execute_query("SELECT * FROM flight_details")
    return render_template('bookedticket.html', booked_tickets=booked_tickets)

@app.route('/api/delete_booking/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    try:
        booking_sql = "SELECT flight_id FROM flight_details WHERE id = ?"
        booking_result = execute_query(booking_sql, (booking_id,))
        if not booking_result:
            return jsonify({"success": False, "message": "Booking not found."}), 404
        flight_id = booking_result[0]['flight_id']
        
        delete_sql = "DELETE FROM flight_details WHERE id = ?"
        rows_affected = execute_query(delete_sql, (booking_id,))
        
        if rows_affected > 0:
            update_seats_sql = "UPDATE flights SET available_seates = available_seates + 1 WHERE flight_id = ?"
            execute_query(update_seats_sql, (flight_id,))
            updated_flight_details = execute_query("SELECT * FROM flights WHERE flight_id = ?", (flight_id,))
            return jsonify({"success": True, "message": "Booking deleted successfully", "flight_details": updated_flight_details}), 200
        else:
            return jsonify({"success": False, "message": "Booking not found."}), 404
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": "An error occurred while deleting the booking."}), 500


@app.route('/finalize_booking', methods=['POST'])
def finalize_booking():
    create_flight_details_table()

    print("Form Data:", request.form)
    passenger_details = request.form.to_dict()

    flight_details = session.get('flight_details', {})
    print("***********************************")
    print(flight_details)
    sql = "UPDATE flights SET available_seates=available_seates-1 WHERE origin_city=? AND destination_city=? AND airline=?"
    params = (flight_details['origin_city'], flight_details['destination_city'], flight_details['airline'])
    execute_query(sql, params)

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO flight_details (flight_id, name, email, seat_id, origin_city, destination_city, 
                    airline, depart_date, no_of_connections, duration, baggage_info, price) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                    flight_details.get('flight_id',''),
                    passenger_details.get('name', ''),
                    passenger_details.get('email', ''),
                    passenger_details.get('seatId', ''),
                    flight_details.get('origin_city', ''),
                    flight_details.get('destination_city', ''),
                    flight_details.get('airline', ''),
                    flight_details.get('depart_date', ''),
                    flight_details.get('NoofConnection', ''),
                    flight_details.get('Duration', ''),
                    flight_details.get('BaggageInfo', ''),
                    flight_details.get('price', '')
                ))
    connection.commit()
    connection.close() 

    try:
        gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
        directions = gmaps.directions(flight_details['origin_city'], flight_details['destination_city'], mode="driving")
        distance = directions[0]['legs'][0]['distance']['text']
        travel_duration = directions[0]['legs'][0]['duration']['text']
        route_steps = [step['html_instructions'] for step in directions[0]['legs'][0]['steps']]
        polyline = directions[0]['overview_polyline']['points']
        origin_coord = f"{directions[0]['legs'][0]['start_location']['lat']},{directions[0]['legs'][0]['start_location']['lng']}"
        dest_coord = f"{directions[0]['legs'][0]['end_location']['lat']},{directions[0]['legs'][0]['end_location']['lng']}"
        map_url = f"https://maps.googleapis.com/maps/api/staticmap?size=550x620&path=enc:{polyline}&key={GOOGLE_MAPS_API_KEY}"
        all_attractions = get_nearby_attractions(dest_coord, GOOGLE_MAPS_API_KEY)
        limited_attractions = all_attractions[:10]
        weather_info = get_weather_info(flight_details['destination_city'], OPENWEATHER_API_KEY)
        converted_price = flight_details.get('converted_price', flight_details.get('price'))
        currency_code = flight_details.get('currency', 'USD')

        return render_template(
            'finalize_booking.html',
            flight_details=flight_details,
            passenger_details=passenger_details,
            distance=distance,
            travel_duration=travel_duration,
            route_steps=route_steps,
            map_url=map_url,
            attractions=limited_attractions,
            weather=weather_info,
            converted_price=converted_price,
            currency_code=currency_code,
            timezone_offset=timezone_offset
        )
    except Exception as e:
        error_message = f"Error occurred: {e}"
        return render_template('error.html', error_message=error_message)