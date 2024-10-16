import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# question 1 taking in parameter in key and body both
@app.route(route="http_example")
def http_example(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')


    req_body = req.get_json()
    name = req_body.get('name')
    chapter = req.params.get('Chapter')

    if name and chapter:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully., {chapter}.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )



# question 2 taking in parameter in keys
@app.route(route="http_example_key")
def http_example_key(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    num1 = req.params.get('num1')
    num2 = req.params.get('num2')

   
    if num1 and num2:
        return func.HttpResponse(f"The sum of {num1} and {num2} is {int(num1) + int(num2)}.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass two numbers in the query string or in the request body for a sum calculation.",
             status_code=200
        )




# question 3 taking in parameter in body part
@app.route(route="http_example_body")
def http_example_body(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
 
    data = req.get_json()
    num1 = data.get('num1')
    num2 = data.get('num2')

    if num1 and num2:
        return func.HttpResponse(f"The sum of {num1} and {num2} is {int(num1) + int(num2)}.")
    
