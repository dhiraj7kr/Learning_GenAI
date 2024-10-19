import logging
import os
import json  # Make sure to import json
from openai import AzureOpenAI
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    query = req.params.get('query')
    if not query:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            query = req_body.get('query')

    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-06-01",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )

    response = client.embeddings.create(
        input=query,
        model=os.getenv("emb_model"),
        dimensions=1536
    ).data[0].embedding

    vector_query = VectorizedQuery(vector=response, k_nearest_neighbors=3, fields="vector")
    search_client = SearchClient(endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"), index_name=os.getenv("AZURE_SEARCH_INDEX"), credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY"))
    )
    results = search_client.search(
        search_text=None,
        vector_queries=[vector_query],
        select=["content"]
    )

    formatted_results = ""
    for idx, result in enumerate(results):
        formatted_results += f"{idx + 1}. {result['content']}\n"

    gptresponse = client.chat.completions.create(
        model=os.getenv("gpt_model"),
        messages=[
            {"role": "system", "content": f'You are an Assistant who give answers based on these results {formatted_results}, if the answer is not found in the results then return ##ANSNOTFOUND##'},
            {"role": "user", "content": query}
        ],
        temperature=0.7,
        max_tokens=300
    )

    output =gptresponse.choices[0].message.content

    if query:
        return func.HttpResponse(
            json.dumps({"response" : output }),
            mimetype="application/json",
            status_code=200
        )
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
        )
