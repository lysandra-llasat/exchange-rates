import requests
from flask import jsonify
from app.config import Config


def fetch_rates_from_api(date):
    """
    Récupère les taux de change depuis l'API pour une date donnée.
    
    :param date: La date pour laquelle récupérer les taux (format YYYY-MM-DD)
    :return: Un dictionnaire des taux de change ou None en cas d'erreur
    """
    url = f"{Config.BASE_URL}{date}.json?app_id={Config.API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
        
        data = response.json()
        
        if 'rates' in data:
            return data['rates']  # Retourne le dictionnaire des taux de change
        
        return None
    
    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

