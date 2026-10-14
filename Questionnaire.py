import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.title("Questionnaire Test Produit - Wise Ultra Running")

# Connexion à Google Sheets
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
    produit = st.selectbox(
        "Quel produit testez-vous ?", 
        ["Sélectionner...", "short", "top", "bottom", "veste"]
    )
    
    if produit != "Sélectionner...":
        confort = st.slider("Évaluez le confort du produit (1 à 5) :", min_value=1, max_value=5, value=3, step=1)
        
        # Enregistrement avec des champs vides pour les questions de durabilité (pour garder le tableur propre)
        st.session_state.responses = {
            "nature_test": nature_test, 
            "produit": produit, 
            "confort": confort,
            "km_parcourus": "",
            "nb_lavages": "",
            "exigences": "",
            "commentaires": ""
        }

elif nature_test == "Test de durabilité":
    # Liste des produits basés sur le catalogue Wise Ultra Running
    liste_produits_wise = [
        "Sélectionner...", 
        "Blackshell ³ (Veste)", 
        "Thermalshell 222 / 333", 
        "Tight 330 (Pantalon)", 
        "Short 122", 
        "T-shirt 230", 
        "Rainshell Pants", 
        "Belt 500 (Ceinture)", 
        "Running Bag 333 (Sac 12L)"
    ]
    
    produit = st.selectbox("Quel produit Wise Ultra Running testez-vous ?", liste_produits_wise)
    
    if produit != "Sélectionner...":
        col1, col2 = st.columns(2)
        with col1:
            km_parcourus = st.number_input("Nombre de km parcourus :", min_value=0, step=10)
        with col2:
            nb_lavages = st.number_input("Nombre de lavages effectués :", min_value=0, step=1)
            
        confort = st.slider("Évaluez le confort du produit (1 à 5) :", min_value=1, max_value=5, value=3, step=1, key="conf_dura")
        exigences = st.slider("Le produit répond-il à vos exigences (1 à 5) ?", min_value=1, max_value=5, value=3, step=1)
        
        commentaires = st.text_area("Avez-vous des remarques détaillées à nous faire partager ? (Optionnel)")
        
        st.session_state.responses = {
            "nature_test": nature_test, 
            "produit": produit, 
            "confort": confort,
            "km_parcourus": km_parcourus,
            "nb_lavages": nb_lavages,
            "exigences": exigences,
            "commentaires": commentaires
        }

# --- STEP 3 : Validation et envoi vers Google Sheets ---
if nature_test in ["Test de fonctionnalité", "Test de durabilité"]:
    # On n'affiche le bouton que si un produit a bien été sélectionné dans l'une ou l'autre des branches
    if st.session_state.responses.get("produit") and st.session_state.responses.get("produit") != "Sélectionner...":
        if st.button("Envoyer mes réponses"):
            try:
                # Lecture des 7 colonnes du tableur existant
                existing_data = conn.read(worksheet="Feuille 1", usecols=list(range(7)), ttl=5)
                existing_data = existing_data.dropna(how="all")
                
                # Ajout de la nouvelle ligne
                new_row = pd.DataFrame([st.session_state.responses])
                updated_data = pd.concat([existing_data, new_row], ignore_index=True)
                
                # Mise à jour sur Google Sheets
                conn.update(worksheet="Feuille 1", data=updated_data)
                st.success("✅ Vos réponses ont été envoyées et enregistrées avec succès !")
            except Exception as e:
                st.error(f"Une erreur est survenue lors de l'envoi : {e}")
