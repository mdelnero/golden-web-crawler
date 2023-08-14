from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)
from datetime import datetime
import openai
import json
import requests
import textwrap

openai.organization = ""
openai.api_key = ""

def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   embeddings = openai.Embedding.create(input = [text], model=model)
   return [x['embedding'] for x in embeddings['data']]

x= get_embedding("Qual a sequencia de lixas para fazer o polimento do carro durante uma restauração")

connections.connect(alias="default", host='localhost', port='19530')
collection = Collection("LangChainCollection")


search_params = {"metric_type": "L2", "params": {"nprobe": 10}}

results = collection.search(data=x, anns_field="vector", param=search_params, limit=3, expr=None, output_fields=['title', 'text'])

for i, hit in enumerate(results):
  print('Results:')
  for ii, hits in enumerate(hit):
      print('\t' + 'Rank:', ii + 1, 'Score:', hits.score, 'Title:', hits.entity.get('title'))
      print(textwrap.fill(hits.entity.get('text'), 88))
      print()