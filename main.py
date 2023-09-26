import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
from scryfallAPI import fetch_card, MaximumRequestDone, WrongCardName, get_bulk_data
from naive_bayes_machine_learning import get_dataframe, analyze

st.set_page_config(layout="wide")
sns.set_theme()

if "vect" not in st.session_state:
     st.session_state.vect = None

if "model" not in st.session_state:
    st.session_state.model = None

data = get_bulk_data()
df = get_dataframe(data)

if "data" not in st.session_state:
    st.session_state.data = data

if "df" not in st.session_state:
    st.session_state.df = df

date1 = st.sidebar.date_input("Choose the Release Dates for the Data you want to use.", value=datetime.datetime.now(),
                              min_value=datetime.date(1993, 11, 1))
date1 = pd.to_datetime(date1)
date2 = st.sidebar.date_input("Choose a second Date to compare the Data.", value=datetime.datetime.now(),
                              min_value=datetime.date(1993, 11, 1))
date2 = pd.to_datetime(date2)
name = st.sidebar.text_input("Card Name", placeholder="Write a Card Name.")

class_name_mapping = {'': 'Colorless',
                      'B': 'Black',
                      'G': 'Green',
                      'R': 'Red',
                      'U': 'Blue',
                      'W': 'White'}

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

st.subheader("Complete Card Dataframe")
btn1 = st.button("Press this button to show the entire Dataframe")
if btn1:
    st.dataframe(df, width=1600)

#st.subheader("Pair Plot")
#with st.expander("Click to show Pair Plot"):
#    sns.set(style="ticks")
#    g = sns.pairplot(df, hue='Colors')
#    st.pyplot(g)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(f"Model for {date1}")
    filtered_df_date1 = df[df['Release Date'] <= date1]
    st.session_state.model, st.session_state.vect = analyze(filtered_df_date1)
    #st.session_state.model, st.session_state.vect = analyze(df[df['Release Date'] <= date1])

    text1 = col1.text_input("Which color is this text most likely to be part of?", key="t1",
                          value="Destroy target Creature")

    if st.session_state.model is not None and st.session_state.vect is not None:
        propas = st.session_state.model.predict_proba(st.session_state.vect.transform([text1]))

        for i in range(len(st.session_state.model.classes_)):
            original_class_name = st.session_state.model.classes_[i]
            new_class_name = class_name_mapping.get(original_class_name, original_class_name)
            st.markdown(f"**{new_class_name}**: {propas[0][i] * 100:.2f} % ")

with col2:
    st.subheader(f"Model for {date2}")
    filtered_df_date2 = df[df['Release Date'] <= date2]
    st.session_state.model, st.session_state.vect = analyze(filtered_df_date2)
    #st.session_state.model, st.session_state.vect = analyze(df[df['Release Date'] <= date2])

    text2 = col2.text_input("Which color is this text most likely to be part of?", key="t2",
                          value="Draw a Card")

    if st.session_state.model is not None and st.session_state.vect is not None:
        propas = st.session_state.model.predict_proba(st.session_state.vect.transform([text2]))

        for i in range(len(st.session_state.model.classes_)):
            original_class_name = st.session_state.model.classes_[i]
            new_class_name = class_name_mapping.get(original_class_name, original_class_name)
            st.markdown(f"**{new_class_name}**: {propas[0][i] * 100:.2f} % ")