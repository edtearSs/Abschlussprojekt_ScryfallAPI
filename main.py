import datetime

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
from scryfallAPI import fetch_card, MaximumRequestDone, WrongCardName
from naive_bayes_machine_learning import get_dataframe, analyze

st.set_page_config(layout="wide")
sns.set_theme()

col1, col2 = st.columns([1, 1])

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

date1 = st.sidebar.date_input("Choose the Release Dates for the Data you want to use.", value=datetime.datetime.now(),
                              min_value=datetime.date(1993, 11, 1))
date2 = st.sidebar.date_input("Choose a second Date to compare the Data.", value=datetime.datetime.now(),
                              min_value=datetime.date(1993, 11, 1))
name = st.sidebar.text_input("Card Name", placeholder="Write a Card Name.")

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

btn1 = st.button("Press this button to show the entire Dataframe")
if btn1:
    st.dataframe(st.session_state.data, width=1600)

class_name_mapping = {'': 'Colorless',
                      'B': 'Black',
                      'G': 'Green',
                      'R': 'Red',
                      'U': 'Blue',
                      'W': 'White'}

with col1:
    st.session_state.model, st.session_state.vect = analyze()

    text1 = col1.text_input("Which color is this text most likely to be part of?", key="t1",
                          value="Destroy target Creature")

    if st.session_state.model != None and st.session_state.vect != None:
        propas = st.session_state.model.predict_proba(st.session_state.vect.transform([text1]))

        for i in range(len(st.session_state.model.classes_)):
            original_class_name = st.session_state.model.classes_[i]
            new_class_name = class_name_mapping.get(original_class_name, original_class_name)
            st.markdown(f"**{new_class_name}**: {propas[0][i] * 100:.2f} % ")

with col2:
    st.session_state.model, st.session_state.vect = analyze()

    text2 = col2.text_input("Which color is this text most likely to be part of?", key="t2",
                          value="Draw a Card")

    if st.session_state.model != None and st.session_state.vect != None:
        propas = st.session_state.model.predict_proba(st.session_state.vect.transform([text2]))

        for i in range(len(st.session_state.model.classes_)):
            original_class_name = st.session_state.model.classes_[i]
            new_class_name = class_name_mapping.get(original_class_name, original_class_name)
            st.markdown(f"**{new_class_name}**: {propas[0][i] * 100:.2f} % ")