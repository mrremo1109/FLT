from flask import Flask, render_template, request
import sqlite3
import logging

app = Flask(__name__)
app.debug = False

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def execute_query(sql):
    conn = get_db_connection()
    res = conn.execute(sql).fetchall()
    conn.commit()
    conn.close()
    return res

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    origin_city = request.args.get('originCity')
    destination_city = request.args.get('destinationCity')
    sql = f"SELECT * FROM flights WHERE origin_city='{origin_city}' AND destination_city='{destination_city}' AND depart_date>=DATE('now')"
    flights = execute_query(sql)
    return render_template('search.html', flights=flights)

@app.route('/bookingdetails', methods=['POST'])
def bookingdetails():
    flight_details = request.form.to_dict()
    return render_template('bookingdetails.html', flight_details=flight_details)

@app.route('/finalize_booking', methods=['POST'])
def finalize_booking():
    try:
        flight_details = request.form.to_dict()
        sql = f"UPDATE flights SET available_seates=available_seates-1 WHERE origin_city='{flight_details['origin_city']}' AND destination_city='{flight_details['destination_city']}' AND airline='{flight_details['airline']}'"
        print(sql)
        execute_query(sql)
        print(flight_details)
        return render_template('finalize_booking.html', flight_details=flight_details)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return "An error occurred while processing your booking request. Please try again later.", 500
