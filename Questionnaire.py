# 📋 Questionnaire interactif en Streamlit

# link : https://questionnairerecuperation-ukukyvl5ihefzuv5fajy7n.streamlit.app/

import streamlit as st
import pandas as pd
import os
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from io import StringIO

def save_to_google_sheets(data: dict):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    

    creds_dict = json.loads(st.secrets["GOOGLE_SHEETS_CREDENTIALS"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    # URL de TA feuille Google Sheets (remplace par la tienne)
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1OaZAif6W_dVp6ScCc9VAG-tH6DNpJNpxp2EsbqEpi4w/edit")
    worksheet = sheet.sheet1

    # Ajouter l'en-tête si première fois
    if worksheet.row_count == 0:
        worksheet.append_row(list(data.keys()))

    # Ajouter la réponse
    row = [str(data.get(k, "")) for k in data.keys()]
    worksheet.append_row(row)

######################################################
################## QUESTIONNAIRE #####################
######################################################

st.set_page_config(page_title="Questionnaire - Récupération Sportive")
st.title("Questionnaire sur la récupération sportive")

# Chemin du fichier CSV
CSV_PATH = "C:/Users/33783/OneDrive/Documents/Documents/INSEP/Travail/Médiation/reponses_questionnaire.csv"

# Fonction d'enregistrement
def save_response(data):
    df = pd.DataFrame([data])
    if os.path.exists(CSV_PATH):
        df.to_csv(CSV_PATH, mode='a', index=False, header=False)
    else:
        df.to_csv(CSV_PATH, index=False)

# Dictionnaire des réponses
reponses = {"timestamp": datetime.now().isoformat()}

# Q1
statut = st.radio("1. 1-Quel est votre statut ?", ["Athlète", "Entraîneur", "Membre d'un staff"])
reponses["Statut"] = statut

# Q2
sport = st.radio("2. 2-Quel est votre sport principal ?", [
    "Athlétisme", "Aviron", "Badminton", "Basketball", "Boxe Anglaise", "Breaking",
    "Canoë Kayak", "Escrime", "Gymnastique", "Haltérophilie", "Handisport", "Judo",
    "Lutte", "Natation", "Pentathlon moderne", "Taekwendo", "Tennis de table",
    "Tir", "Tir à l'arc", "Autre"])
# Q3 si Autre
if sport =="Autre":
    sport = st.text_input("Vous avez répondu \"Autre\". Précisez svp :")
reponses["Sport"] = sport




# Q4
age = st.radio("4. Quel est votre tranche d'âge ?", [
    "Moins de 18 ans", "Entre 18 et 25 ans", "Entre 26 et 30 ans",
    "Entre 31 et 35 ans", "36 ans ou plus"])
reponses["Tranche d'âge"] = age

# Q5
connaissance = st.slider("5. Comment évaluez-vous vos connaissances en matière de récupération sportive ?", 1, 10)
reponses["Connaissance récup"] = connaissance

# Q6 - Classement (simulé avec multiselect)
#elements = ["Nutrition", "Méditation", "Étirements", "Hydratation", "Massage", "Sommeil", "Récupération active", "Electrostimulation", "Techniques d'immersion"]
#classement = st.multiselect("6. Classez les éléments essentiels de la récupération (ordre décroissant d'importance)", elements)
#reponses["Classement récup"] = classement

# Q7
importance = st.slider("7. Quelle place accordez-vous à la récupération dans une optique de performance ?", 1, 10)
reponses["Importance récup"] = importance

# Branche Athlète : Q8 -> Q12
if statut == "Athlète":
    reponses["Branche"] = "Athlète"
    reponses["Note sommeil /10"] = st.slider("8. Comment estimez-vous vos habitudes de sommeil ?", 1, 10)
    reponses["Note alimentation /10"] = st.slider("9. Comment estimez-vous vos habitudes en terme de nutrition/hydratation ?", 1, 10)

    techniques = st.radio("10. Quelles techniques de récupération utilisez-vous parmi celles ci-dessous ?", [
        "Rouleau de massage", "Pistolet de massage", "Bains", "Cryothérapie",
        "Electrostimulation", "Méditation", "Récupération active", "Aucune"])
    reponses["Techniques utilisées"] = techniques

    frequence = st.radio("11. Fréquence d'utilisation des techniques ?", [
        "Jamais", "1 fois par mois", "1 fois par semaine", "2 à 3 fois par semaine",
        "4 à 5 fois par semaine", "Tous les jours"])
    reponses["Fréquence d'utilisation"] = frequence

    coach_conseil = st.radio("12. Recevez-vous des conseils de votre entraîneur au sujet de la récupération ?", [
        "Non, jamais", "Oui, parfois", "Oui, très souvent"])
    reponses["Conseils du coach reçus ?"] = coach_conseil

else:
    # Branche Entraîneur ou Staff : Q13 -> Q16
    reponses["Branche"] = "Coach/Staff"
    recup_planif = st.radio("13. Intégrez-vous la récupération à la planification de vos athlète ?", [
        "Non, jamais", "Oui, une fois par semaine", "Oui, plusieurs fois par semaine", "Oui, tous les jours"])
    reponses["Intégration à la planif ?"] = recup_planif

    suivi = st.radio("14. Effectuez-vous un suivi auprès de vos athlètes pour contrôler leur récupération ?", [
        "Non, jamais", "Oui, parfois", "Oui, régulièrement"])
    reponses["Suivi effectué ?"] = suivi

    if suivi != "Non, jamais":
        comment = st.text_input("15. Comment ?")
        reponses["Comment ?"] = comment

    info_donnee = st.radio("16. Pensez-vous informer suffisamment vos athlètes au sujet de la récupération ?", [
        "Non, et ce n'est pas mon rôle", "Non, mais j'aimerais pouvoir le faire davantage", "Oui, je pense que c'est suffisant"])
    reponses["Informez-vous assez ?"] = info_donnee

# Q17
interet = st.radio("17. Aimeriez-vous être davantage informé au sujet de la récupération ?", [
    "Non, ça ne m'intéresse pas", "Oui, sur les fondamentaux(nutrition ,hydratation, sommeil)",
    "Oui, sur les techniques de récupération", "Oui, sur la planification de la récupération",
    "Oui, sur le suivi des athlètes", "Oui, sur les nouvelles technologies",
    "Oui, sur les études scientifiques", "Autre"])
reponses["Voulez-vous plus d'infos ?"] = interet

if "Autre" in interet:
    autre_interet = st.text_input("18. Vous avez répondu \"Autre\". Précisez :")
    reponses["Plus d'infos (autre) ?"] = autre_interet

# Q19
moyen = st.radio("19. Par quel moyen souhaitez-vous être informé ?", [
    "Articles scientifiques", "Articles vulgarisés", "Fiches méthodes", "Conférences",
    "Ateliers pratiques", "Vidéos/podcasts", "Réseaux sociaux", "Autre"])
reponses["Par quel moyen ?"] = moyen

if "Autre" in moyen:
    autre_moyen = st.text_input("20. Vous avez répondu \"Autre\". Précisez :")
    reponses["Autres moyens"] = autre_moyen

# Q21
commentaire = st.text_area("21. Quelque chose à ajouter ?")
reponses["Commentaires"] = commentaire

# Bouton d'envoi
if st.button("Envoyer mes réponses"):
    #save_response(reponses)
    save_to_google_sheets(reponses)
    st.success("Merci pour votre participation ! 🎉")
