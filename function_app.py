from azure.storage.blob import BlobServiceClient
import azure.functions as func
import logging
#from io import StringIO
import pandas as pd
import numpy as np
import json
#import os
import io

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.function_name("pythonfunction")
@app.route(route="pythonfunction", methods=["GET", "POST"],auth_level=func.AuthLevel.ANONYMOUS)   # FUNCTION
def pythonfunction_def(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('======Pythonfunction HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            req_body = {}
        name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
        )

# Fonction 1 : Calculer le max
@app.function_name("max_function")
@app.route(route="max_function", methods=["POST"],auth_level=func.AuthLevel.ANONYMOUS)  # Added the decorator here
def max_function_def(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Execution de la fonction Azure: max_function...")

    try:
        # import
        #from azure.storage.blob import BlobServiceClient
        from io import StringIO
        #import pandas as pd
        #import json
        import os
        #
        # Vérifiez si les données JSON sont bien reçues
        req_body = req.get_json()
        blob_name = req_body.get('file')
        column = req_body.get('column')

        # Vérifiez la récupération des paramètres
        logging.info(f"Nom du fichier: {blob_name}")
        logging.info(f"Nom de la colonne: {column}")

        # Assurez-vous que le fichier et la colonne sont fournis
        if not blob_name or not column:
            return func.HttpResponse("Paramètres 'file' ou 'column' manquants.", status_code=400)

        # calcul du mean
        # Connexion au Blob Storage
        connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_name = "test21container"
        
        # Accéder au blob (fichier CSV)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_data = blob_client.download_blob().content_as_text()

        # Charger les données CSV dans un DataFrame pandas
        df = pd.read_csv(StringIO(blob_data))
        
        # Vérifier si la colonne existe dans le fichier
        if column not in df.columns:
            return func.HttpResponse("La colonne spécifiée n'existe pas dans le fichier.", status_code=400)
        
        # Calculer le max pour la colonne spécifiée
        mean_value = str(df[column].max())
        result = {"max": mean_value}  # Remplacez avec la logique réelle
        return func.HttpResponse(json.dumps(result), status_code=200, mimetype="application/json")

    except ValueError:
        return func.HttpResponse("Erreur : données JSON invalides.", status_code=400)
    except Exception as e:
        logging.error(f"Erreur : {str(e)}")
        return func.HttpResponse(f"Erreur : {str(e)}", status_code=500)


# Fonction 2 : Calculer la moyenne
@app.function_name("mean_function")
@app.route(route="mean_function", methods=["POST"],auth_level=func.AuthLevel.ANONYMOUS)  # Added the decorator here
def mean_function_def(req: func.HttpRequest) -> func.HttpResponse:
    #
    logging.info("Execution de la fonction Azure: mean_function...")

    try:
        # Vérifiez si les données JSON sont bien reçues
        req_body = req.get_json()
        blob_name = req_body.get('file')
        column = req_body.get('column')

        # Vérifiez la récupération des paramètres
        logging.info(f"Nom du fichier: {blob_name}")
        logging.info(f"Nom de la colonne: {column}")

        # Assurez-vous que le fichier et la colonne sont fournis
        if not blob_name or not column:
            return func.HttpResponse("Paramètres 'file' ou 'column' manquants.", status_code=400)

        # calcul du mean
        # Connexion au Blob Storage
        connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_name = "test21container"
        
        # Accéder au blob (fichier CSV)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_data = blob_client.download_blob().content_as_text()

        # Charger les données CSV dans un DataFrame pandas
        df = pd.read_csv(StringIO(blob_data))
        
        # Vérifier si la colonne existe dans le fichier
        if column not in df.columns:
            return func.HttpResponse("La colonne spécifiée n'existe pas dans le fichier.", status_code=400)
        
        # Calculer la moyenne pour la colonne spécifiée
        mean_value = str(df[column].mean())
        result = {"mean": mean_value}  # Remplacez avec la logique réelle
        return func.HttpResponse(json.dumps(result), status_code=200, mimetype="application/json")

    except ValueError:
        return func.HttpResponse("Erreur : données JSON invalides.", status_code=400)
    except Exception as e:
        logging.error(f"Erreur : {str(e)}")
        return func.HttpResponse(f"Erreur : {str(e)}", status_code=500)


# Fonction 3 : Calculer la moyenne des éléments de la liste values = [2,4,4,2] par exemple
@app.function_name("test_function")
@app.route(route="test_function", methods=["GET", "POST"],auth_level=func.AuthLevel.ANONYMOUS)   # FUNCTION
def test_function_d(req: func.HttpRequest) -> func.HttpResponse:
    #
    # Configurer le logger
    logging.basicConfig(level=logging.DEBUG)
    
    # Exemple de log avec différents niveaux
    logging.debug("Ceci est un message de débogage.")
    logging.info("Ceci est un message d'information.")
    logging.warning("Ceci est un message d'avertissement.")
    logging.error("Ceci est un message d'erreur.")
    logging.critical("Ceci est un message critique.")
    
    # Log de la requête entrante
    logging.info(f"Requête reçue avec les paramètres : {req.params}")
    
    try:
        # test 
        #import numpy as np  # Importer NumPy
        
        # Récupération des données de la requête

        # Initialisation
        values = [2,4,4,2]
        
        # Utiliser NumPy pour calculer la moyenne
        mean_value = np.mean(values)
        result = {'mean': mean_value}  # Résultat avec NumPy
        
        logging.info(f"Calcul réussi avec résultat : {result}")
        
        # Retourner une réponse JSON avec le résultat
        return func.HttpResponse(
            json.dumps(result),  # Convertir le dictionnaire en JSON
            mimetype="application/json",  # Spécifier le type de contenu comme JSON
            status_code=200
        )
    
    except ValueError as ve:
        logging.error(f"Erreur de validation : {str(ve)}")
        return func.HttpResponse(f"Erreur: {str(ve)}", status_code=400)
    
    except Exception as e:
        logging.error(f"Erreur lors du calcul : {str(e)}")
        return func.HttpResponse(f"Erreur: {str(e)}", status_code=500)


# anotherfunction
@app.function_name("anotherfunction")
@app.route(route="anotherfunction", methods=["POST"],auth_level=func.AuthLevel.ANONYMOUS)  # Added the decorator here
def anotherfunction(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Anotherfunction HTTP trigger function processed a request.')

    return func.HttpResponse(
        "This is another HTTP triggered function.",
        status_code=200
    )

# anotherfunction
@app.function_name("anotherfunction2")
@app.route(route="anotherfunction2", methods=["POST"],auth_level=func.AuthLevel.ANONYMOUS)  # Added the decorator here
def anotherfunction2(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Anotherfunction2222 HTTP trigger function processed a request.')

    return func.HttpResponse(
        "This is another HTTP triggered function.22222",
        status_code=200
    )
