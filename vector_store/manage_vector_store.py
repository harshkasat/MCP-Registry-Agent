import os
from langchain_pinecone import PineconeVectorStore
from vector_store.config import create_pinecone_index
from config.google_gemini import LangchainGeminiClient
from langchain.schema import Document
from typing import List


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
            # print("@@ METADATA ",retreive)
            return retreive[0].page_content
        except Exception as error:
            print(f"An error occurred while creating documents at PineconeVectorStoreManage().retrieve_query(): {error}")

