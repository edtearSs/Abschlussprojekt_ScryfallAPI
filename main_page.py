
from matplotlib import widgets
import streamlit as st

import scryfall
import main
import data
import ml
import ds
import git


st.set_page_config(layout="wide")

st.title("Abschlussprojekt Data-Science Institut")  #

pages = {
    "1. Scryfall": scryfall,
    "1. Main": main,
    "2. Daten": data,
    "3. Machine-Learning": ml,
    "4. Data-Science": ds,
    "5. Git-Hub": git,
}

st.sidebar.title("Seiten")
select = st.sidebar.radio("Gehe zu Seite:", list(pages.keys()))
pages[select].app()
