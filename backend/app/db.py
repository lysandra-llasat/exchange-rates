import mysql.connector
from .config import Config

def get_db_connection():
    return mysql.connector.connect(
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        database=Config.DB_NAME
    )

def insert_or_update_rate(date, base_currency, target_currency, rate):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO exchange_rates (date, base_currency, target_currency, rate) 
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE rate = %s
        """, (date, base_currency, target_currency, rate, rate))
        connection.commit()
    finally:
        cursor.close()
        connection.close()

def get_rates_by_date(date, base_currency):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT target_currency, rate FROM exchange_rates 
            WHERE date = %s AND base_currency = %s
        """, (date, base_currency))
        rates = cursor.fetchall()
        return {rate['target_currency']: rate['rate'] for rate in rates}
    finally:
        cursor.close()
        connection.close()
