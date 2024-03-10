from flask import Flask, render_template, request, jsonify
import json
import sqlite3
from datetime import datetime
import os
print(os.getcwd())
import requests

APIapp = Flask(__name__)

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
        res = cursor.fetchall()
    else:
        conn.commit()
        res = None
    cursor.close()
    conn.close()
    return res

@APIapp.route('/api/Duration', methods=['GET', 'POST'])
def get_Duration():
    # 1. Fetch data from the database
    sql = "SELECT Duration FROM flights"  # Modify the query as needed
    Duration_data = execute_query(sql)

    # 2. Check if data is retrieved successfully
    if not Duration_data:
        return jsonify({"error": "No flights data found"}), 404  # Return error for not found
    
    # 3. Return the Duration_data
    return jsonify(Duration_data)