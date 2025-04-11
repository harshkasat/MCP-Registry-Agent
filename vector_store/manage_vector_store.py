import os
from langchain_pinecone import PineconeVectorStore
from vector_store.config import create_pinecone_index
from config.google_gemini import LangchainGeminiClient
from dotenv import load_dotenv
from langchain.schema import Document
from typing import List
load_dotenv()


# def load_document(embeddings, index, chunks):
#     try:
#         # Generate UUIDs for each document
#         uuids = [str(uuid4()) for _ in range(len(chunks))]
#         vector_store = PineconeVectorStore(index=index, embedding=embeddings)
#         vector_store.add_documents(documents=chunks, ids=uuids)
#         print(f"Documents loaded successfully into Pinecone index {index}")

#     except Exception as e:
#         print(f"An error occurred while loading documents into Pinecone: {e}")

# def load_vector_store(index_name, embeddings):
#     vstore = Pinecone.from_existing_index(index_name=index_name, embedding=embeddings)
#     print(f"Successfully loaded document from vectors store into memory at index {index_name}")
#     return vstore

class PineconeVectorStoreManage:

    def __init__(self,
                index_name='mcp-server', 
                embeddings=LangchainGeminiClient().generate_embeddings()):

        self.index = create_pinecone_index(index_name=index_name)
        self.vectorstore = PineconeVectorStore(index=self.index, embedding=embeddings)

    def create_documents(self, documents: List[Document], batch_size: int = 50):
        try:
            for i in range(0, len(documents), batch_size):
                batch = documents[i:i + batch_size]
                self.vectorstore.add_documents(batch)

            print(f"Documents successfully added in batches of {batch_size}")
            return self.vectorstore
        except Exception as error:
            print(f"An error occurred while creating documents at PineconeVectorStoreManage().create_documents(): {error}")

    def retrieve_query(self, _query:str):
        try:
            retreive = self.vectorstore.similarity_search(_query)
            return retreive[0].page_content
        except Exception as error:
            print(f"An error occurred while creating documents at PineconeVectorStoreManage().retrieve_query(): {error}")
