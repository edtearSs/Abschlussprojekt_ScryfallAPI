import streamlit as st

def app():
    base = '''
    import requests

    CARD_URL = "https://api.scryfall.com/cards/named?fuzzy"

    class WrongCardName(Exception):
        pass

    class MaximumRequestDone(Exception):
        pass
    '''
    fetch_card = '''
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
    '''
    bulk_data = '''
    def get_bulk_data():
        try:
            url = f"https://api.scryfall.com/bulk-data"
            print(f"making request to {url}")
            data = requests.get(url)
            bulk_data_list = data.json()['data']
    
            for item in bulk_data_list:
                if item['description'] == 'A JSON file containing one Scryfall card object for each Oracle ID on' \ 
                                          'Scryfall. The chosen sets for the cards are an attempt to return the most' \ 
                                          'up-to-date recognizable version of the card.':
                    download_url = item['download_uri']  
                    bulk_data = requests.get(download_url).json()  
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
    '''
    st.header("Imports und Klassenerstellung")
    st.code(base, language='python')
    st.write("'fuzzy' in der URL beeinflusst das Suchverhalten. 'exact' = genauer Name / 'fuzzy' = ungenauer Name")
    st.header("Funktion um einzelne Karten mithilfe der API zu requesten")
    st.code(fetch_card, language='python')
    st.header("Funktion um Bulk-Data von Scryfall zu bekommen.")
    st.code(bulk_data, language='python')
    st.write("Bulk Data selbst ist ein JSON-file der mit einer 'for' Schleife gefiltert werden muss.")
