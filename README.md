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


---

# Text Search and Retrieval with Embedding Similarity Using Azure OpenAI

This project demonstrates how to search and retrieve relevant text from a dataset by generating and comparing embeddings using **Azure OpenAI**. It uses cosine similarity to rank the relevance of the text in relation to a user query, then constructs a prompt for further interaction with OpenAI's **GPT model**.

## Project Overview

The script performs the following tasks:

1. **Loading Embeddings**: Reads text and pre-generated embeddings from a CSV file.
2. **Query Embedding Generation**: Creates an embedding for the user query using Azure OpenAI’s embedding model.
3. **Cosine Similarity Comparison**: Compares the query embedding with existing embeddings in the dataset to find the most relevant text.
4. **Contextual Prompt Construction**: Prepares a system prompt with the relevant text and sends it along with the user query to Azure OpenAI's GPT model.
5. **Chat Completion**: Uses Azure's GPT model to generate a response based on the provided context and user query.

## Key Features

- **Embedding-based Search**: The script uses embeddings to compare the similarity between the query and stored text.
- **Cosine Similarity**: Implements cosine similarity to find the most relevant pieces of text.
- **Azure OpenAI GPT Integration**: Provides a response based on the relevant text, using Azure OpenAI's GPT model for natural language processing.

## Dependencies

- `openai`: For generating text embeddings and GPT-based completions via Azure OpenAI.
- `pandas`: For handling and reading the CSV file.
- `ast`: For safely evaluating string representations of embeddings in the CSV file.
- `scipy`: For calculating cosine similarity between embeddings.

### Installation

1. Install the required libraries by running:
   ```bash
   pip install pandas openai scipy
   ```

2. Configure your **Azure OpenAI** endpoint and API key:
   - Obtain an API key and endpoint from your **Azure OpenAI** account.
   - Replace the placeholders `<endpoint>` and `<api-key>` in the script with your actual Azure OpenAI credentials.

3. Ensure your **CSV file** is ready with the text and its corresponding embeddings. The CSV structure should be as follows:

| text                       | embeddings                                |
|----------------------------|-------------------------------------------|
| "Attendance policy info..." | [0.12, 0.53, 0.64, ...]                   |
| "Leave policy details..."   | [0.75, 0.24, 0.89, ...]                   |
| ...                         | ...                                       |

### Project Structure

```
.
├── script.py                # Main Python script for the project
├── vector.csv               # CSV file containing text and embeddings
├── README.md                # Project documentation
```

### Script Breakdown

#### 1. Generating Embeddings for Query

The `generate_embedding` function takes in a user query (or any text), sends it to the Azure OpenAI API, and returns the embedding.

```python
def generate_embedding(text):
    emb = embedding_client.embeddings.create(model="text-embedding-3-small",input=text)
    res = json.loads(emb.model_dump_json())
    return res['data'][0]['embedding']
```

#### 2. Loading Embeddings from CSV

The script loads the existing text and embeddings from `vector.csv`. The `embeddings` column is parsed using the `ast.literal_eval` function to convert string representations back into Python lists.

```python
df = pd.read_csv("vector.csv", index_col=False)
df['embeddings'] = df['embeddings'].apply(ast.literal_eval)
```

#### 3. Calculating Cosine Similarity

Cosine similarity is used to determine the relatedness between the query embedding and each text embedding in the CSV. The most relevant text is selected by sorting the similarities in descending order.

```python
relatedness_fn = lambda x, y: 1 - scipy.spatial.distance.cosine(x, y)
 
strings_and_relatednesses = [
    (row['text'], relatedness_fn(input_embedding, row['embeddings']))
    for i, row in df.iterrows()
]
 
strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
```

#### 4. Constructing a System Prompt

The script selects the top `N` most relevant texts (in this case, 2) and constructs a system prompt to provide context to the GPT model.

```python
content = ""
for text in strings[:top]:
    content += text + "\n"

system_prompt = f"""
                context:
                ---
                {content}
                ---
                """
```

#### 5. Querying Azure OpenAI's GPT Model

Finally, the script sends both the system prompt and user query to the GPT model, which generates a response.

```python
message_text = [{"role":"system", "content": system_prompt}, {"role":"user", "content": query}]
completion = embedding_client.chat.completions.create(
    model="gpt-35-turbo-16k",
    messages= message_text,
    temperature=0
)
```

#### 6. Outputting the Result

The response generated by GPT is printed for the user:

```python
print(completion.choices[0].message.content)
```

### Example Usage

1. Prepare your **CSV file** with text and pre-generated embeddings. Ensure that it’s named `vector.csv` and placed in the same directory as the script.

2. Update the **Azure OpenAI endpoint** and **API key** in the script.

3. Run the script:

```bash
python script.py
```

4. The script will take your query, such as:

   ```plaintext
   "What is the attendance leave policy?"
   ```

5. It will output the most relevant content based on the embeddings in the CSV, followed by the GPT model's response:

   ```plaintext
   According to the attendance policy, leave requests must be submitted at least 24 hours in advance. Any leave exceeding 5 days requires approval from the HR department.
   ```

### Notes

- **CSV Preparation**: If you haven't generated embeddings for your text, you can use the same `generate_embedding` function to generate and store embeddings in the CSV format before running the query search.
- **Custom Models**: This script uses the `gpt-35-turbo-16k` and `text-embedding-3-small` models from Azure. Ensure your Azure subscription supports these models.
  
### License

This project is licensed under the MIT License. You are free to modify and use it according to your needs.




