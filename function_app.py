from azure.storage.blob import BlobServiceClient
import azure.functions as func
import logging
#from io import StringIO
import pandas as pd
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

# anotherfunction
@app.function_name("anotherfunction")
@app.route(route="anotherfunction", methods=["POST"],auth_level=func.AuthLevel.ANONYMOUS)  # Added the decorator here
def anotherfunction(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Anotherfunction HTTP trigger function processed a request.')

    return func.HttpResponse(
        "This is another HTTP triggered function.",
        status_code=200
    )
