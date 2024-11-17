import streamlit as st
import requests

# URL des Azure Functions
MEAN_FUNCTION_URL = "https://testrl22.azurewebsites.net/api/mean_function"
MAX_FUNCTION_URL = "https://testrl22.azurewebsites.net/api/max_function"
TEST_FUNCTION_URL = "https://testrl22.azurewebsites.net/api/test_function"

# Titre de l'application Streamlit
st.title("Calcul de Moyenne et Max d'une Colonne CSV sur Blob Storage")

# Nom du fichier et colonne avec valeurs par défaut
blob_name = st.text_input("Nom du fichier CSV dans Blob Storage", value="test1.csv")
column = st.text_input("Nom de la colonne", value="c1")

# Fonction pour afficher la réponse ou l'erreur
def display_response(response, key):
    st.write("Statut de la réponse :", response.status_code)
    if response.status_code == 200:
        result = response.json()
        st.write(f"{key} : {result[key]}")
    else:
        st.write("Réponse brute :", response.text)  # Afficher le texte de l'erreur
        st.error("Erreur : " + response.text)

# Bouton pour calculer la moyenne
if st.button("Calculer Moyenne"):
    data = {'file': blob_name, 'column': column}
    headers = {"Content-Type": "application/json"}
    response = requests.post(MEAN_FUNCTION_URL, json=data, headers=headers)
    display_response(response, "mean")

# Bouton pour calculer le maximum
if st.button("Calculer Maximum"):
    data = {'file': blob_name, 'column': column}
    headers = {"Content-Type": "application/json"}
    response = requests.post(MAX_FUNCTION_URL, json=data, headers=headers)
    display_response(response, "max")

# Bouton pour tester l'appel de TEST_FUNCTION_URL
if st.button("For test ---> Appel de l'Azure Function: TEST_FUNCTION()"):
    headers = {"Content-Type": "application/json"}
    response = requests.post(TEST_FUNCTION_URL, headers=headers)
    if response.status_code == 200:
        result = response.json()
        st.write(f"Réponse de test : {result}")
    else:
        st.write("Réponse brute :", response.text)
        st.error("Erreur lors de l'appel de la fonction de test : " + response.text)
