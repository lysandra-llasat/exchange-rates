import mysql.connector
from .config import Config  # Utilise un import relatif

def get_db_connection():
    """Retourne une connexion à la base de données."""
    connection = mysql.connector.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME
    )
    return connection

def insert_or_update_rate(timestamp, base, target_currency_code, rate):
    """Insère ou met à jour un taux de change dans la base de données."""
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO exchange_rates (date, base_currency, target_currency, rate) 
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE rate = %s
        """, (timestamp, base, target_currency_code, rate, rate))
        connection.commit()
    except mysql.connector.Error as e:
        raise
    finally:
        cursor.close()
        connection.close()

def get_rates_by_date(date):
    """Récupère les taux de change pour une date donnée."""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT base_currency, target_currency, rate FROM exchange_rates WHERE date = %s", (date,))
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as e:
        raise
    finally:
        cursor.close()
        connection.close()
