import requests
import json

BASE_URL = "https://api.scryfall.com"

class WrongCardName(Exception):
    pass

class MaximumRequestDone(Exception):
    pass

def fetch_card(name):
    try:
        url = f"{BASE_URL}/{name}"
        print(f"making request to {url}")
        data = requests.get(url)
        return data.json()

    except ValueError as e:
        print(data.text)
        if "maximum number" in data.text:
            raise MaximumRequestDone
        if "card does not exist." in data.text:
            raise WrongCardName
    except requests.exceptions.RequestException as e:
        print (f"Request Error: {e}")
        return None