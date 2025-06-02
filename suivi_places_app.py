import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Fichier CSV des données
FILENAME = "suivi_places.csv"

# Charger les données ou créer un DataFrame vide
if os.path.exists(FILENAME):
    df = pd.read_csv(FILENAME)
else:
    st.error("Le fichier CSV est introuvable.")
    st.stop()

st.title("📊 Suivi de tes places Parcoursup")

# Formulaire pour ajouter une nouvelle entrée
with st.form("formulaire"):
    st.subheader("📝 Entrer les places du jour")
    today = datetime.today().strftime('%Y-%m-%d')
    date = st.text_input("Date (YYYY-MM-DD)", value=today)

    colonnes = df.columns.tolist()
    colonnes.remove("Date")

    new_data = {}
    for col in colonnes:
        place = st.number_input(f"{col}", min_value=0, step=1, format="%d")
        new_data[col] = place

    submitted = st.form_submit_button("Enregistrer")
    if submitted:
        if date in df["Date"].values:
            st.warning("Une entrée existe déjà pour cette date.")
        else:
            ligne = {"Date": date}
            ligne.update(new_data)
            df = pd.concat([df, pd.DataFrame([ligne])], ignore_index=True)
            df.to_csv(FILENAME, index=False)
            st.success("Données enregistrées avec succès.")

# Afficher les données
st.subheader("📅 Historique des données")
st.dataframe(df.sort_values(by="Date", ascending=False))

# Choisir une ou plusieurs formations à afficher
st.subheader("📈 Visualiser l'évolution")
formations = df.columns.tolist()
formations.remove("Date")
choix = st.multiselect("Choisis les formations à afficher :", formations, default=formations[:3])

if choix:
    fig, ax = plt.subplots(figsize=(10, 5))
    for formation in choix:
        ax.plot(df["Date"], df[formation], label=formation)
    ax.set_xlabel("Date")
    ax.set_ylabel("Position")
    ax.invert_yaxis()  # Plus près de 1 = meilleur rang
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.info("Sélectionne au moins une formation pour afficher un graphique.")
