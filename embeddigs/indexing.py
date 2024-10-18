import PyPDF2
import pandas as pd
from openai import AzureOpenAI
import json
 
embedding_client = AzureOpenAI(azure_endpoint="<endpiont>",
                               api_key="<api-key>",
                               api_version="2024-02-01")
 
def extract_text_from_pdf(pdf_path):
    with open(pdf_path,'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        text_per_page = []
        for page_num in range(num_pages) :
            page = reader.pages[page_num]
            text_per_page.append(page.extract_text())
    return text_per_page
 
pdf_path ='AttendancePolicy.pdf'
text_per_page = extract_text_from_pdf(pdf_path)
 
def generate_embedding(text):
    emb = embedding_client.embeddings.create(model="text-embedding-3-small",input=text)
    res = json.loads(emb.model_dump_json())
    return res['data'][0]['embedding']
 
csv_file_path = 'vector.csv'
try:
    df = pd.read_csv(csv_file_path)
except FileNotFoundError:
    df = pd.DataFrame(columns=['text','embeddings'])
 
new_df = pd.DataFrame({'text': text_per_page })
 
df = pd.concat([df, new_df], ignore_index=True)
 
df['embeddings'] = df['text'].apply(generate_embedding)
 
df.to_csv(csv_file_path,index=False)
