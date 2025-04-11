import time
import getpass
import os

from pinecone import Pinecone, ServerlessSpec

pinecone_api_key = os.getenv('PINECONE_API_KEY')


def create_pinecone_index(index_name:str):
    try:
        pc = Pinecone(api_key=pinecone_api_key)

        existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

        if index_name not in existing_indexes:
            pc.create_index(
                name=index_name,
                dimension=768,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
            while not pc.describe_index(index_name).status["ready"]:
                time.sleep(1)

        index = pc.Index(index_name)

        return index
    except Exception as error:
        print(f"Failed to create pinecone index Lcreate_pinecone_index(): {error}")
