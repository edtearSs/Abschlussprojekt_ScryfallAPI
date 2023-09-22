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

def analyze(keywords):
    df = get_dataframe()

    vect = CountVectorizer()
    wordsCountArray = vect.fit_transform(df['Oracle Text'])

    X_train, X_test, y_train, y_test = train_test_split(wordsCountArray, df['Colors'], test_size=0.2, random_state=0)

    model = MultinomialNB()
    model.fit(X_train, y_train)

    # Calculate the likelihood of each color for the given keywords
    keyword_text = " ".join(keywords)
    keyword_vector = vect.transform([keyword_text])

    likelihood = model.predict_proba(keyword_vector)
    colors = model.classes_

    s = f"Likelihood of Colors for Keywords: {', '.join(keywords)}\n\n"

    for color, prob in zip(colors, likelihood[0]):
        s += f"{color}: {prob * 100:.2f}%\n"

    st.markdown(s)

    return model, vect

# Example usage:
#selected_keywords = ["power", "toughness"]  # Replace with your chosen keywords
#model, vect = analyze(selected_keywords)