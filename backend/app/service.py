import requests
from .config import Config

def fetch_rates_from_api(date):
    """
    Fetch exchange rates from the API for a specific date.
    
    :param date: The date for which to fetch the rates (format YYYY-MM-DD)
    :return: Dictionary of exchange rates or None if there's an error
    """
    api_key = Config.API_KEY
    url = f'{Config.API_URL}/historical/{date}.json?app_id={api_key}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  
        
        print(f'Response status code: {response.status_code}')
        print(f'Response body: {response.text}')
        
        api_data = response.json()
        
        # Ensure that the 'rates' key is in the API response
        if 'rates' in api_data:
            return api_data['rates']
        else:
            print('No "rates" key in API response.')
            return None
    except requests.RequestException as e:
        # Log the error or handle it as needed
        print(f'Error fetching data from API: {str(e)}')
        return None
