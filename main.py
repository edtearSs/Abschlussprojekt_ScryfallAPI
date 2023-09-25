import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scryfallAPI import fetch_card, MaximumRequestDone, WrongCardName
from naive_bayes_machine_learning import get_dataframe, analyze

st.set_page_config(layout="wide")
sns.set_theme()

col1, col2 = st.columns(2)

if "vect" not in st.session_state:
    # Der Vectorizer für unser Model
    # (https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html)
    st.session_state.vect = None

if "model" not in st.session_state:
    # Das Modell, ein Naive Bayes
    # (https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html#sklearn.naive_bayes.MultinomialNB)
    st.session_state.model = None

if "data" not in st.session_state:
    # Hier muss der Dataframe in den session state aufgenommen werden
    st.session_state.data = get_dataframe()

name = st.sidebar.text_input("Kartenname", placeholder="Schreib hier einen Kartennamen.")
print(name)

if name:
    try:
        data = fetch_card(name.lower())
        st.sidebar.write(data)
    except MaximumRequestDone:
        st.error("Maximum number of requests reached. Please try again later.")
    except WrongCardName:
        st.error("The provided Pokemon name is not valid.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

with col1:

    st.dataframe(st.session_state.data, width=800)

with col2:
    st.session_state.model, st.session_state.vect = analyze()

    text = st.text_input("Which color is this text most likely to be part of?")

    if st.session_state.model != None and st.session_state.vect != None:
        propas = st.session_state.model.predict_proba(st.session_state.vect.transform([text]))

        for i in range(len(st.session_state.model.classes_)):
            st.markdown(f"**{st.session_state.model.classes_[i]}**: {propas[0][i]*100:.2f} % ")