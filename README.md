# GenAI
### FUNCTIONS

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



---

# PDF Text Extraction and Embedding Generation

This project demonstrates how to extract text from a PDF document, generate text embeddings using OpenAI’s Azure API, and save the text and corresponding embeddings to a CSV file.

## Project Overview

The script performs the following steps:
1. Extracts text from each page of a PDF document using **PyPDF2**.
2. Generates text embeddings for each page using **Azure OpenAI’s embedding API**.
3. Saves the text and its corresponding embeddings into a CSV file using **pandas**.

## Key Features

- **Text Extraction from PDF**: Reads each page of a PDF and extracts the text content.
- **Embedding Generation**: Utilizes Azure OpenAI API to generate embeddings for the extracted text.
- **CSV File Handling**: Stores the extracted text and its embeddings in a CSV file, ensuring that if the CSV already exists, it appends new data without overwriting previous entries.

## Dependencies

The following Python libraries are required for this project:

- `PyPDF2`: For extracting text from the PDF document.
- `pandas`: For handling and manipulating the data.
- `openai`: For generating text embeddings through Azure OpenAI.
- `json`: To handle JSON data.

### Installation

1. Install the required libraries using pip:
   ```bash
   pip install PyPDF2 pandas openai
   ```

2. Configure the Azure OpenAI endpoint and API key:
   - Set up your Azure OpenAI account and obtain an API key and endpoint.
   - Replace the placeholders `<endpoint>` and `<api-key>` in the script with your actual Azure OpenAI details.

### Project Structure

```
.
├── script.py                # Python script to extract text and generate embeddings
├── AttendancePolicy.pdf      # Example PDF file to extract text from
├── vector.csv               # Output CSV file containing text and embeddings
└── README.md                # Project documentation
```

### Script Breakdown

#### 1. Extracting Text from PDF

The `extract_text_from_pdf` function uses `PyPDF2` to read and extract text from each page of the PDF file.

```python
def extract_text_from_pdf(pdf_path):
    with open(pdf_path,'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        text_per_page = []
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text_per_page.append(page.extract_text())
    return text_per_page
```

#### 2. Generating Embeddings

The `generate_embedding` function sends the text data to the Azure OpenAI API to generate embeddings. It uses the `text-embedding-3-small` model to create an embedding for each page of text.

```python
def generate_embedding(text):
    emb = embedding_client.embeddings.create(model="text-embedding-3-small",input=text)
    res = json.loads(emb.model_dump_json())
    return res['data'][0]['embedding']
```

#### 3. Combining Data and Saving to CSV

The script handles existing CSV files to avoid overwriting previous data. If the file doesn’t exist, it creates a new one. It adds the extracted text and the generated embeddings to the CSV.

```python
csv_file_path = 'vector.csv'
try:
    df = pd.read_csv(csv_file_path)
except FileNotFoundError:
    df = pd.DataFrame(columns=['text','embeddings'])

new_df = pd.DataFrame({'text': text_per_page })

df = pd.concat([df, new_df], ignore_index=True)

df['embeddings'] = df['text'].apply(generate_embedding)

df.to_csv(csv_file_path, index=False)
```

### Usage Example

1. Place the PDF file (e.g., `AttendancePolicy.pdf`) in the same directory as the script.
2. Run the script:
   ```bash
   python script.py
   ```
3. The script will:
   - Extract text from each page of the PDF.
   - Generate embeddings for the text.
   - Save the text and embeddings in the `vector.csv` file.

The resulting `vector.csv` will look like this:

| text                       | embeddings                                |
|----------------------------|-------------------------------------------|
| "Page 1 content..."         | [0.1, 0.2, 0.3, ...]                      |
| "Page 2 content..."         | [0.5, 0.7, 0.8, ...]                      |
| ...                         | ...                                       |

---

### Notes

- Ensure that the Azure OpenAI service is properly configured and that your API key and endpoint are correct.
- The embeddings generated by Azure OpenAI can be used in various downstream tasks, such as text similarity, clustering, or semantic search.

### License

This project is licensed under the MIT License. Feel free to modify and use it for your own needs.

---


