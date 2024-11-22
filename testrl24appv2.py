import azure.functions as func
import logging

app = func.FunctionApp()


@app.function_name("pythonfunction")
@app.route(route="pythonfunction", methods=["POST"])
def pythonfunction(req: func.HttpRequest) -> func.HttpResponse:
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


@app.function_name("anotherfunction")
@app.route(route="anotherfunction", methods=["POST"])  # Added the decorator here
def anotherfunction(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Anotherfunction HTTP trigger function processed a request.')

    return func.HttpResponse(
        "This is another HTTP triggered function.",
        status_code=200
    )
