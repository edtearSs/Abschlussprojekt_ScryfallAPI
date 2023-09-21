import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scryfallAPI import fetch_card, MaximumRequestDone, WrongCardName

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