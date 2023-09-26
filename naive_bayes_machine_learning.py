import streamlit as st
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

from scryfallAPI import get_bulk_data

def get_dataframe(data):
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
        released_at = currentItem.get("released_at", "")

        # Create a list of colors as a string
        color_str = ', '.join(colors)

        rows.append([card_name, mana_cost, oracle_text, color_str, color_identity, rarity, type_line, released_at])


    # Create a DataFrame from the list of rows
    df = pd.DataFrame(rows, columns=["Card Name", "Mana Cost", "Oracle Text", "Colors", "Color Identity", "Rarity",
                                     "Type Line", "Release Date"])

    filtered_df = df[~df['Type Line'].apply(lambda x: 'token' in x.lower()
                                                      or 'card' in x.lower() or 'scheme' in x.lower()
                                                      or 'vanguard' in x.lower() or 'emblem' in x.lower()
                                                      or 'hero' in x.lower() or 'conspiracy' in x.lower()
                                                      or 'phenomenon' in x.lower() or 'stickers' in x.lower()
                                                      or 'summon' in x.lower() or 'tolkien' in x.lower()
                                                      or 'plane — ' in x.lower())]

    # Reset the index of the filtered DataFrame
    filtered_df.reset_index(drop=True, inplace=True)

    # Create a copy of the filtered DataFrame before dropping rows
    filtered_df_copy = filtered_df.copy()

    # Drop rows with missing values in specified columns
    df = filtered_df_copy.dropna(axis='index', subset=['Oracle Text'])

    # Print the DataFrame
    return df

def analyze(df):
    # Create a separate DataFrame for single-colored cards
    single_color_df = df[df['Colors'].apply(lambda x: len(x.split(', ')) == 1)]

    single_color_df = single_color_df.drop(['Card Name', 'Mana Cost', 'Color Identity', 'Rarity', 'Type Line'], axis=1)
    #st.dataframe(single_color_df, width=700)

    vect = CountVectorizer()
    wordsCountArray = vect.fit_transform(single_color_df['Oracle Text'])

    X_train, X_test, y_train, y_test = train_test_split(wordsCountArray, single_color_df['Colors'], test_size=0.2, random_state=0)

    model = MultinomialNB()
    model.fit(X_train, y_train)

    s = f"Model trained for {X_train.shape[0]} single-colored cards. \n\n"
    s += f"Model Accuracy: {model.score(X_test, y_test) * 100:.2f}%"

    st.markdown(s)

    return model, vect
