from flask import Blueprint, request, jsonify
import requests
import mysql.connector
from .config import Config
from .db import insert_or_update_rate, get_rates_by_date, get_db_connection

bp = Blueprint('main', __name__)

@bp.route('/reload_data', methods=['POST'])
def reload_data():
    data = request.get_json()
    date = data.get('date')
    base_currency = data.get('base_currency')
    target_currency = data.get('target_currency')

    # Vérifier que tous les paramètres nécessaires sont présents
    if not date or not base_currency or not target_currency:
        return jsonify({'error': 'Date, base currency, and target currency are required'}), 400

    # Construire l'URL de la requête API
    api_key = Config.API_KEY
    url = f'{Config.API_URL}/historical/{date}.json?app_id={api_key}&base={base_currency}&symbols={target_currency}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({'error': f'Failed to fetch data from API: {str(e)}'}), 500

    # Extraire les taux de change de la réponse API
    api_data = response.json()
    rate = api_data['rates'].get(target_currency)

    # Insérer ou mettre à jour le taux de change dans la base de données
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
