import streamlit as st
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

from scryfallAPI import get_bulk_data

def get_dataframe():
    data = get_bulk_data()
    #print(data)
    rows = []

    # Iterate through the data and append rows to the list
    for currentItem in data:
        card_name = currentItem.get("name", "")
        mana_cost = currentItem.get("mana_cost", "")
        oracle_text = currentItem.get("oracle_text", "")
        colors = currentItem.get("colors", [])
        color_identity = currentItem.get("color_identity", [])
        rarity = currentItem.get("rarity", "")
        type_line = currentItem.get("type_line", "")

        rows.append([card_name, mana_cost, oracle_text, colors, color_identity, rarity, type_line])

    # Create a DataFrame from the list of rows
    df = pd.DataFrame(rows, columns=["Card Name", "Mana Cost", "Oracle Text", "Colors", "Color Identity", "Rarity", "Type Line"])

    # Print the DataFrame
    #print(df)
    return df