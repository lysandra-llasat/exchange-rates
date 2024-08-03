import os

class Config:
    # Configuration de la base de données
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'votre_nouveau_mot_de_passe')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'exchange_rates_db')
    DEBUG = True
    
    # URL de l'API
    API_URL = os.getenv('API_URL', 'https://openexchangerates.org/api')
    API_KEY = os.getenv('API_KEY', 'b51fb011a53749d799c5777b57315c82')  # Remplace par ta clé API
