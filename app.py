from flask import Flask, render_template, request
import sqlite3
import googlemaps
import requests

app = Flask(__name__)
app.debug = False

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def execute_query(sql, params=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if params:
        cursor.execute(sql, params)
    else:
        cursor.execute(sql)
    if sql.strip().lower().startswith('select'):
        # This is a SELECT query, so we should fetch the results
        res = cursor.fetchall()
    else:
        # This is not a SELECT query, so there are no results to fetch
        conn.commit()
        res = None
    cursor.close()
    conn.close()
    return res

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    origin_city = request.args.get('originCity')
    destination_city = request.args.get('destinationCity')
    sql = "SELECT * FROM flights WHERE origin_city=? AND destination_city=? AND depart_date>=DATE('now')"
    flights = execute_query(sql, (origin_city, destination_city))
    return render_template('search.html', flights=flights)

@app.route('/bookingdetails', methods=['POST'])
def bookingdetails():
    flight_details = request.form.to_dict()
    return render_template('bookingdetails.html', flight_details=flight_details)

GOOGLE_MAPS_API_KEY = 'AIzaSyCHfcbLvLze_Uz57qc1Wl4H1TWQ2E_dv5E'
OPENWEATHER_API_KEY = '9cc7cb0d46d0878a0faa22cecf727c72' 


def get_nearby_attractions(dest_coord, api_key):
    # Google Places API - Nearby Search request
    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': dest_coord,
        'radius': '5000',  # Search within a 5 km radius
        'type': 'tourist_attraction',
        'key': api_key
    }
    response = requests.get(endpoint_url, params=params)
    if response.status_code == 200:
        attractions = response.json()['results']
    else:
        attractions = []
    return attractions

def get_weather_info(city_name, openweather_api_key):
    # OpenWeatherMap API request
    endpoint_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': openweather_api_key,
        'units': 'metric'  # For temperature in Celsius
    }
    response = requests.get(endpoint_url, params=params)
    if response.status_code == 200:
        weather_info = response.json()
    else:
        weather_info = {}
    return weather_info

@app.route('/finalize_booking', methods=['POST'])
def finalize_booking():
    # Part 1: Update flight availability
    flight_details = request.form.to_dict()
    sql = "UPDATE flights SET available_seates=available_seates-1 WHERE origin_city=? AND destination_city=? AND airline=?"
    params = (flight_details['origin_city'], flight_details['destination_city'], flight_details['airline'])
    execute_query(sql, params) 
    # Assuming execute_query is a function that executes the SQL command
    
    # Part 2: Generate directions and map
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
    directions = gmaps.directions(flight_details['origin_city'], flight_details['destination_city'], mode="driving")

    distance = directions[0]['legs'][0]['distance']['text']
    route_steps = [step['html_instructions'] for step in directions[0]['legs'][0]['steps']]
    polyline = directions[0]['overview_polyline']['points']
    origin_coord = f"{directions[0]['legs'][0]['start_location']['lat']},{directions[0]['legs'][0]['start_location']['lng']}"
    dest_coord = f"{directions[0]['legs'][0]['end_location']['lat']},{directions[0]['legs'][0]['end_location']['lng']}"
    map_url = f"https://maps.googleapis.com/maps/api/staticmap?size=550x620&path=enc:{polyline}&key={GOOGLE_MAPS_API_KEY}"
    all_attractions = get_nearby_attractions(dest_coord, GOOGLE_MAPS_API_KEY)
    limited_attractions = all_attractions[:10]
    weather_info = get_weather_info(flight_details['destination_city'], OPENWEATHER_API_KEY)

    # Render template with all the information
    return render_template(
        'finalize_booking.html',
        flight_details=flight_details,
        distance=distance,
        route_steps=route_steps,
        map_url=map_url,
        attractions=limited_attractions,
        weather=weather_info
    )