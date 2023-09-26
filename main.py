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

date1 = st.sidebar.date_input("Choose the Release Date for the Data you want to use.", value=datetime.date(2000, 11, 1),
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
        card = fetch_card(name.lower())
        image_url = card.get("image_uris").get("normal")
        if image_url:
            st.sidebar.image(image_url, caption=name.upper())
        st.sidebar.write("Oracle Text:", card.get("oracle_text"))
        st.sidebar.write("Mana Cost:", card.get("mana_cost"))
        st.sidebar.write("Rarity:", card.get("rarity"))
        st.sidebar.write("Type Line:", card.get("type_line"))
        st.sidebar.write("Latest Print/Reprint:", card.get("set_name"))
        st.sidebar.write(card)
    except MaximumRequestDone:
        st.error("Maximum number of requests reached. Please try again later.")
    except WrongCardName:
        st.error("The provided Pokemon name is not valid.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

st.subheader("Complete Card Dataframe")
with st.expander("Click to show Dataframe"):
    st.dataframe(df, width=1600)
    # st.write(df.dtypes)

# st.subheader("Pair Plot")
# with st.expander("Click to show Pair Plot"):
#     sns.set(style="ticks")
#     df['Colors'] = df['Colors'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
#     df['Color Identity'] = df['Color Identity'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
#     st.write(df.head(30))
#     sns.pairplot(data=df)

df['Release Date'] = pd.to_datetime(df['Release Date'])

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(f"Model for {date1}")
    filtered_df_date1 = df[df['Release Date'] <= date1]
    st.session_state.model, st.session_state.vect = analyze(filtered_df_date1)
    # st.session_state.model, st.session_state.vect = analyze(df[df['Release Date'] <= date1])

    text1 = col1.text_input("Which color is this text most likely to be part of?", key="t1",
                            value="Draw a card")

    if st.session_state.model is not None and st.session_state.vect is not None:
        propas = st.session_state.model.predict_proba(st.session_state.vect.transform([text1]))

        for i in range(len(st.session_state.model.classes_)):
            original_class_name = st.session_state.model.classes_[i]
            new_class_name = class_name_mapping.get(original_class_name, original_class_name)
            st.markdown(f"**{new_class_name}**: {propas[0][i] * 100:.2f} % ")

    # sns.pairplot(filtered_df_date1)

with col2:
    st.subheader(f"Model for {date2}")
    filtered_df_date2 = df[df['Release Date'] <= date2]
    st.session_state.model, st.session_state.vect = analyze(filtered_df_date2)
    # st.session_state.model, st.session_state.vect = analyze(df[df['Release Date'] <= date2])

    text2 = col2.text_input("Which color is this text most likely to be part of?", key="t2",
                            value="Draw a Card")

    if st.session_state.model is not None and st.session_state.vect is not None:
        propas = st.session_state.model.predict_proba(st.session_state.vect.transform([text2]))

        for i in range(len(st.session_state.model.classes_)):
            original_class_name = st.session_state.model.classes_[i]
            new_class_name = class_name_mapping.get(original_class_name, original_class_name)
            st.markdown(f"**{new_class_name}**: {propas[0][i] * 100:.2f} % ")

    # sns.pairplot(filtered_df_date2)
