import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.title("Questionnaire Test Produit")

# Connexion à Google Sheets (le lien URL sera fourni via les secrets plus tard)
conn = st.connection("gsheets", type=GSheetsConnection)

# Initialisation du stockage des réponses
if "responses" not in st.session_state:
    st.session_state.responses = {}

# --- STEP 1 : Tronc commun ---
nature_test = st.radio(
    "Quelle est la nature du test ?",
    ["Sélectionner...", "Test de fonctionnalité", "Test de durabilité"]
)

# --- STEP 2 : Logique conditionnelle ---
if nature_test == "Test de fonctionnalité":
    produit = st.selectbox("Quel produit testez-vous ?", ["Sélectionner...", "short", "top", "bottom", "veste"])
    
    if produit != "Sélectionner...":
        confort = st.slider("Évaluez le confort du produit (1 à 5) :", min_value=1, max_value=5, value=3, step=1)
        # On met des champs vides pour les infos entreprise pour ne pas décaler le tableur
        st.session_state.responses = {"nature_test": nature_test, "produit": produit, "confort": confort, "societe": "", "effectif": ""}

elif nature_test == "Test de durabilité":
    societe = st.text_input("Nom de votre entreprise :")
    effectif = st.number_input("Nombre de salariés :", min_value=1, step=1)
    
    # On met des champs vides pour le produit pour ne pas décaler le tableur
    st.session_state.responses = {"nature_test": nature_test, "produit": "", "confort": "", "societe": societe, "effectif": effectif}

# --- STEP 3 : Validation et envoi vers Google Sheets ---
if nature_test in ["Test de fonctionnalité", "Test de durabilité"]:
    if st.button("Envoyer mes réponses"):
        try:
            # 1. On lit les données qui existent déjà dans le tableur
            existing_data = conn.read(worksheet="Feuille 1", usecols=list(range(5)), ttl=5)
            existing_data = existing_data.dropna(how="all")
            
            # 2. On prépare la nouvelle ligne de réponse
            new_row = pd.DataFrame([st.session_state.responses])
            updated_data = pd.concat([existing_data, new_row], ignore_index=True)
            
            # 3. On met à jour le Google Sheet
            conn.update(worksheet="Feuille 1", data=updated_data)
            st.success("✅ Vos réponses ont été envoyées et enregistrées avec succès !")
        except Exception as e:
            st.error(f"Une erreur est survenue lors de l'envoi : {e}")
