# GenAI
#Function

Azure Functions HTTP Example
This repository contains examples of Azure Functions that demonstrate how to handle HTTP requests with different methods of passing parameters. Each function showcases a specific way to access input data, either through query parameters or request body.

Functions Overview
1. http_example
Route: /http_example
Method: GET
Parameters:
Body: JSON object containing a name.
Query String: Chapter parameter.
Description: This function responds with a personalized greeting if both a name in the body and a Chapter in the query string are provided. Otherwise, it returns a default message.
2. http_example_key
Route: /http_example_key
Method: GET
Parameters:
Query String: num1 and num2 parameters.
Description: This function calculates and returns the sum of two numbers provided in the query string. If either parameter is missing, it returns a default message.
3. http_example_body
Route: /http_example_body
Method: GET
Parameters:
Body: JSON object containing num1 and num2.
Description: This function calculates and returns the sum of two numbers provided in the request body. If either number is missing, it does not return a message.
Getting Started
Prerequisites
Python 3.6 or later
Azure Functions Core Tools
An Azure subscription (if you plan to deploy)
Installation
Clone the repository:

bash
Copy code
git clone <repository-url>
cd <repository-directory>
Install the required packages:

bash
Copy code
pip install azure-functions
Running Locally
To run the functions locally:

Make sure you have the Azure Functions Core Tools installed.

Start the local development server:

bash
Copy code
func start
Test the functions using a tool like Postman or curl.

Example Requests
http_example:

Request:

bash
Copy code
curl -X GET "http://localhost:7071/api/http_example?Chapter=1" -H "Content-Type: application/json" -d '{"name":"Alice"}'
Response:

bash
Copy code
Hello, Alice. This HTTP triggered function executed successfully., 1.
http_example_key:

Request:

bash
Copy code
curl -X GET "http://localhost:7071/api/http_example_key?num1=5&num2=10"
Response:

python
Copy code
The sum of 5 and 10 is 15.
http_example_body:

Request:

bash
Copy code
curl -X GET "http://localhost:7071/api/http_example_body" -H "Content-Type: application/json" -d '{"num1":3, "num2":7}'
Response:

python
Copy code
The sum of 3 and 7 is 10.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Contributing
If you'd like to contribute, please fork the repository and submit a pull request.

Acknowledgements
Azure Functions Documentation for guidance on creating and managing Azure Functions
