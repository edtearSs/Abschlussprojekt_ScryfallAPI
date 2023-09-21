import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scryfallAPI import fetch_card, MaximumRequestDone, WrongCardName
from naive_bayes_machine_learning import get_dataframe

st.set_page_config(layout="wide")
sns.set_theme()

name = st.text_input("Kartenname", placeholder="Schreib hier einen Kartennamen.")
print(name)

if name:
    try:
        data = fetch_card(name.lower())
        st.write(data)
    except MaximumRequestDone:
        st.error("Maximum number of requests reached. Please try again later.")
    except WrongCardName:
        st.error("The provided Pokemon name is not valid.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

df = get_dataframe()

# Convert the "Type Line" column to lowercase for case-insensitive comparison
df = get_dataframe()

# Filter rows based on the "Type Line" condition
filtered_word = ['plane']
filtered_df = df[~df['Type Line'].apply(lambda x: x.lower() in filtered_word or 'token' in x.lower()
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
filtered_df_copy.dropna(axis='index', subset=['Oracle Text'], inplace=True)

st.write(filtered_df_copy)