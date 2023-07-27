from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Milvus
from util import *
from webpage import *
import os

os.environ["OPENAI_API_KEY"] = ''

db = MongoAdapter()
embeddings = OpenAIEmbeddings()

def read_all_documents():
    try:        

        # all_documents = db.read_all()
        all_documents = db.read_query({"title": "Puma Classic: Puma GTE 1975 (2) - A restauração"})

        for doc in all_documents:

            title = doc["title"].replace('Puma Classic: ', '')
            text = doc['plain_text']
            metadata = {"title": title, "url": doc["url"]}

            document = [Document(page_content=text, metadata=metadata)]

            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50, separator="\n")
            docs = text_splitter.split_documents(document)

            for doc in docs:
                doc.page_content = title + ' - ' + doc.page_content

            #print(len(text), len(docs))
            vector_db = Milvus.from_documents(docs, embeddings)

    except pymongo.errors.ConnectionFailure:
        print("Failed to connect to MongoDB. Make sure MongoDB is running.")

if __name__ == "__main__":
    read_all_documents()