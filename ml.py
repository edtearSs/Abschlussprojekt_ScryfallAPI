import streamlit as st

def app():
    base = '''
        import streamlit as st
        import pandas as pd

        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.model_selection import train_test_split
        from sklearn.naive_bayes import MultinomialNB
        '''
    dataframe = '''
    def get_dataframe(data):
        rows = []
        progressbar = st.progress(0)
    
        # Iterate through the data and append rows to the list
        for i, currentItem in enumerate(data):
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
            color_identity_str = ', '.join(color_identity)
    
            rows.append([card_name, mana_cost, oracle_text, color_str, color_identity_str, rarity, type_line, released_at])
    
            progressbar.progress((i + 1) / len(data))
    
        progressbar.empty()
    
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
    
        df = df.astype("string")
    
        return df
        '''
    naive_bayes = '''
        def analyze(df):
        # Create a separate DataFrame for single-colored cards
        single_color_df = df[df['Colors'].apply(lambda x: len(x.split(', ')) == 1)]
    
        single_color_df = single_color_df.drop(['Card Name', 'Mana Cost', 'Color Identity', 'Rarity', 'Type Line'], axis=1)
        # st.dataframe(single_color_df, width=700)
    
        vect = CountVectorizer()
        wordsCountArray = vect.fit_transform(single_color_df['Oracle Text'])
    
        X_train, X_test, y_train, y_test = train_test_split(wordsCountArray, single_color_df['Colors'], test_size=0.2,
                                                            random_state=0)
    
        model = MultinomialNB()
        model.fit(X_train, y_train)
    
        s = f"Model trained for {X_train.shape[0]} single-colored cards. \n\n"
        s += f"Model Accuracy: {model.score(X_test, y_test) * 100:.2f}%"
    
        st.markdown(s)
    
        return model, vect
        '''
    st.header("Imports und Module")
    st.code(base, language='python')
    st.header("Umwandlung des JSON files in einen Pandas Dataframe")
    st.code(dataframe, language='python')
    st.write("Die Bulkdaten werden mithilfe einer 'for'-Schleife in einen Pandas Dataframe umgewandelt. ")
    st.write("Gleichzeitig werden uninteressante Kartentypen bereits ausgefiltert.")
    st.header("Training des Machine-Learning Algorithmus")
    st.code(naive_bayes, language='python')
    st.write("Zuerst werden alle Karten die mehr als eine Farbe haben gefiltert.   ")
    st.write("Danach werden alle für den Algorithmus unwichtigen Daten entfernt.")
    st.write("Mit dem CountVectorizer werden die Wörter in der Spalte 'Oracle Text' in ein wordsCountArray umgewandelt.")
    st.write("Im Anschluss wird mit train_test_split ein Trainingsdatensatz anhand von wordsCountArray und den Farben "
             "des Dataframe erstellt und mit Naive_Bayes trainiert.")