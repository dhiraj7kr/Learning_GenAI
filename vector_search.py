import pandas as pd
from openai import AzureOpenAI
import ast, json
import scipy.spatial
 
embedding_client = AzureOpenAI(azure_endpoint="https://openai-azuretesting.openai.azure.com/",
                               api_key="d57bdf8c8fd54d98aea4f20e0a183479",
                               api_version="2024-02-01")
 
def generate_embedding(text):
    emb = embedding_client.embeddings.create(model="text-embedding-3-small",input=text)
    res = json.loads(emb.model_dump_json())
    return res['data'][0]['embedding']
 
relatedness_fn = lambda x,y: 1 - scipy.spatial.distance.cosine(x,y)
 
df = pd.read_csv("vector.csv", index_col=False)
df['embeddings'] = df['embeddings'].apply(ast.literal_eval)
 
query = "what is attenndence leave policy? "
 
top = 2
 
input_embedding = generate_embedding(text=query)
 
strings_and_relatednesses = [
    (row['text'],relatedness_fn(input_embedding,row['embeddings']))
    for i, row in df.iterrows()
]
 
strings_and_relatednesses.sort(key=lambda x : x[1], reverse=True)
strings, relatednesses = zip(*strings_and_relatednesses)
 
content = ""
for text in strings[:top]:
    content+=text + "\n"
   
   
system_prompt = """
 
                context:
                ---
                {content}
                --- """.format(content=content)
               
user_message = query
 
message_text = [{"role":"system", "content": system_prompt},{"role":"user", "content": user_message}]
 
completion = embedding_client.chat.completions.create(
    model="gpt-35-turbo-16k",
    messages= message_text,
    temperature=0
)
 
print(completion.choices[0].message.content)
