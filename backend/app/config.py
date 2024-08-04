import os

class Config:
    DEBUG = True
    # database config
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'votre_nouveau_mot_de_passe')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'exchange_rates_db')
    DEBUG = True
    
    # API URL
    API_URL = os.getenv('API_URL', 'https://openexchangerates.org/api')
    API_KEY = os.getenv('API_KEY', 'b51fb011a53749d799c5777b57315c82') 
    BASE_URL = os.getenv('BASE_URL', 'https://openexchangerates.org/api/historical/')