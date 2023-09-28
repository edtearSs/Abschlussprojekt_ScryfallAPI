import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
from scryfallAPI import fetch_card, MaximumRequestDone, WrongCardName, get_bulk_data
from naive_bayes_machine_learning import get_dataframe, analyze

def app():
    sns.set_theme()

    if "vect" not in st.session_state:
        st.session_state.vect = None

    if "model" not in st.session_state:
        st.session_state.model = None

    if "data" not in st.session_state:
        st.session_state.data = get_bulk_data()

    if "df" not in st.session_state:
        st.session_state.df = get_dataframe(st.session_state.data)

    if "card" not in st.session_state:
        st.session_state.card = {}

    class_name_mapping = {'': 'Colorless',
                          'B': 'Black',
                          'G': 'Green',
                          'R': 'Red',
                          'U': 'Blue',
                          'W': 'White'}

    name = st.sidebar.text_input("Card Name", placeholder="Write a Card Name.")

    if name:
        try:
            if name not in st.session_state.card.keys():

                card = fetch_card(name.upper())
                if card == None:
                    st.error("Abfrage fehlerhaft.")
                else:
                    st.session_state.card[name.upper()] = card

                image_url = st.session_state.card[name.upper()].get("image_uris").get("normal")
                if image_url:
                    st.sidebar.image(image_url, caption=name.upper())
                st.sidebar.subheader("Oracle Text:")
                st.sidebar.write(st.session_state.card[name.upper()].get("oracle_text"))
                st.sidebar.subheader("Mana Cost:")
                st.sidebar.write(st.session_state.card[name.upper()].get("mana_cost"))
                st.sidebar.subheader("Rarity:")
                st.sidebar.write(st.session_state.card[name.upper()].get("rarity"))
                st.sidebar.subheader("Type Line:")
                st.sidebar.write(st.session_state.card[name.upper()].get("type_line"))
                st.sidebar.subheader("Latest Print/Reprint:")
                st.sidebar.write(st.session_state.card[name.upper()].get("set_name"))
                st.sidebar.write(st.session_state.card[name.upper()])

            if name in st.session_state.card.keys():

                image_url = st.session_state.card[name.upper()].get("image_uris").get("normal")
                if image_url:
                    st.sidebar.image(image_url, caption=name.upper())
                st.sidebar.subheader("Oracle Text:")
                st.sidebar.write(st.session_state.card[name.upper()].get("oracle_text"))
                st.sidebar.subheader("Mana Cost:")
                st.sidebar.write(st.session_state.card[name.upper()].get("mana_cost"))
                st.sidebar.subheader("Rarity:")
                st.sidebar.write(st.session_state.card[name.upper()].get("rarity"))
                st.sidebar.subheader("Type Line:")
                st.sidebar.write(st.session_state.card[name.upper()].get("type_line"))
                st.sidebar.subheader("Latest Print/Reprint:")
                st.sidebar.write(st.session_state.card[name.upper()].get("set_name"))
                st.sidebar.write(st.session_state.card[name.upper()])
        except MaximumRequestDone:
            st.error("Maximum number of requests reached. Please try again later.")
        except WrongCardName:
            st.error("The provided Pokemon name is not valid.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    st.subheader("Complete Card Dataframe")
    with st.expander("Click to show Dataframe"):
        st.dataframe(st.session_state.df, width=1600)
        # st.write(df.dtypes)

    # st.subheader("Pair Plot")
    # with st.expander("Click to show Pair Plot"):
    #     df_drop = df.dropna(axis=0)
    #     sns.pairplot(data=df_drop, hue='Colors',
    #                  x_vars=['Mana Cost', 'Colors', 'Rarity'],
    #                  y_vars=['Type Line', 'Release Date'],)

    st.session_state.df['Release Date'] = pd.to_datetime(st.session_state.df['Release Date'])

    st.info("This algorithm only uses single color cards. Multicolor cards are filtered out. The Project is using "
            "CountVectorizer and Naive_Bayes to predict how likely the card text is part of a certain color. The Model "
            "is added twice to the project to be able to filter the Data by Release Date and see the changes in color "
            "Identity over the years. After doing field tests for roughly 100 cards the accuracy is much higher than "
            "it actually shows!")

    col1, col2 = st.columns([1, 1])

    with col1:
        date1 = st.date_input("Choose the Release Date for the Data you want to use.",
                                      value=datetime.date(2000, 11, 1),
                                      min_value=datetime.date(1993, 11, 1))
        date1 = pd.to_datetime(date1)
        st.subheader(f"Model for {date1}")
        filtered_df_date1 = st.session_state.df[st.session_state.df['Release Date'] <= date1]
        st.session_state.model, st.session_state.vect = analyze(filtered_df_date1)

        text1 = col1.text_input("Which color is this text most likely to be part of?", key="t1",
                                value="Draw a card")

        if st.session_state.model is not None and st.session_state.vect is not None:
            propas = st.session_state.model.predict_proba(st.session_state.vect.transform([text1]))

            for i in range(len(st.session_state.model.classes_)):
                original_class_name = st.session_state.model.classes_[i]
                new_class_name = class_name_mapping.get(original_class_name, original_class_name)
                st.markdown(f"**{new_class_name}**: {propas[0][i] * 100:.2f} % ")


    with col2:
        date2 = st.date_input("Choose a second Date to compare the Data to.", value=datetime.datetime.now(),
                                      min_value=datetime.date(1993, 11, 1))
        date2 = pd.to_datetime(date2)
        filtered_df_date2 = st.session_state.df[st.session_state.df['Release Date'] <= date2]
        st.subheader(f"Model for {date2}")
        st.session_state.model, st.session_state.vect = analyze(filtered_df_date2)

        text2 = col2.text_input("Which color is this text most likely to be part of?", key="t2",
                                value="Draw a Card")

        if st.session_state.model is not None and st.session_state.vect is not None:
            propas = st.session_state.model.predict_proba(st.session_state.vect.transform([text2]))

            for i in range(len(st.session_state.model.classes_)):
                original_class_name = st.session_state.model.classes_[i]
                new_class_name = class_name_mapping.get(original_class_name, original_class_name)
                st.markdown(f"**{new_class_name}**: {propas[0][i] * 100:.2f} % ")
