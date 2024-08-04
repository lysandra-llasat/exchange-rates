from flask import Blueprint, request, jsonify
import requests
import mysql.connector
from .config import Config
from .db import insert_or_update_rate, get_rates_by_date, get_db_connection
from .service import fetch_rates_from_api
bp = Blueprint('main', __name__)

@bp.route('/reload_data', methods=['POST'])
def reload_data():
    data = request.get_json()
    date = data.get('date')
    base_currency = data.get('base_currency')
    target_currency = data.get('target_currency')

    # Extract exchange rates from the API response
    if not date or not base_currency or not target_currency:
        return jsonify({'error': 'Date, base currency, and target currency are required'}), 400

    # Build the API request URL
    api_key = Config.API_KEY
    url = f'{Config.API_URL}/historical/{date}.json?app_id={api_key}&base={base_currency}&symbols={target_currency}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({'error': f'Failed to fetch data from API: {str(e)}'}), 500

    #Extract exchange rates from the API response
    api_data = response.json()
    rate = api_data['rates'].get(target_currency)


    db_connection = None
    cursor = None
    try:
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        if rate:
            cursor.execute("""
                INSERT INTO exchange_rates (date, base_currency, target_currency, rate) 
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE rate = %s
            """, (date, base_currency, target_currency, rate, rate))

        db_connection.commit()
    except mysql.connector.Error as e:
        return jsonify({'error': f'Failed to insert data into database: {str(e)}'}), 500
    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()
    
    return jsonify({'message': 'Data reloaded successfully'}), 200

@bp.route('/get_exchange_rates', methods=['GET'])
def get_exchange_rates():
    date = request.args.get('date')
    if not date:
        return jsonify({'error': 'Date is required'}), 400

    # Verify if the exchange rates for this date are present in the database
    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT base_currency, target_currency, rate 
        FROM exchange_rates 
        WHERE date = %s
    """, (date,))
    
    rates = cursor.fetchall()

    if rates:
        rates_dict = {rate['target_currency']: rate['rate'] for rate in rates}
    else:
        # if the exchange rates are not found, retrieve them with the API
        rates_dict = fetch_rates_from_api(date)
        
        if not rates_dict:
            return jsonify({'error': 'No data found for the given date'}), 404

        # Insert the exchange rates into the database
        for target_currency, rate in rates_dict.items():
            insert_or_update_rate(date, 'USD', target_currency, rate)

    response = {
        'date': date,
        'rates': rates_dict
    }

    return jsonify(response)
