import requests
import json

CARD_URL = "https://api.scryfall.com/cards/named?exact"

class WrongCardName(Exception):
    pass

class MaximumRequestDone(Exception):
    pass

def fetch_card(name):
    try:
        url = f"{CARD_URL}={name}"
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
        print(f"Request Error: {e}")
        return None

def get_bulk_data():
    try:
        url = f"https://api.scryfall.com/bulk-data"
        print(f"making request to {url}")
        data = requests.get(url)
        bulk_data_list = data.json()['data']

        for item in bulk_data_list:
            if item['description'] == 'A JSON file containing one Scryfall card object for each Oracle ID on Scryfall.' \
                                      ' The chosen sets for the cards are an attempt to return the most up-to-date' \
                                      ' recognizable version of the card.':
                download_url = item['download_uri']  # Get the download URL of the desired data
                bulk_data = requests.get(download_url).json()  # Download and parse the JSON data
                return bulk_data

        return None
    except ValueError as e:
        print(data.text)
        if "maximum number" in data.text:
            raise MaximumRequestDone
        if "card does not exist." in data.text:
            raise WrongCardName
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return None