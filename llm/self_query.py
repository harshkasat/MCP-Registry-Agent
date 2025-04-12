from langchain.retrievers.self_query.base import SelfQueryRetriever
from config.google_gemini import LangchainGeminiClient
from vector_store.manage_vector_store import PineconeVectorStoreManage
from vector_store.metadata_structure_info import metadata_filed_info


DOCUMENT_CONTENT_DESCRIPTION = "Brief description of the MCP tool or project and its purpose."

def self_query_retriever(query:str, verbose:bool=True):
    try:
        llm = LangchainGeminiClient().generate_content()
        vector_store = PineconeVectorStoreManage().vectorstore

        query_retriever = SelfQueryRetriever.from_llm(
            llm=llm,
            vectorstore=vector_store,
            metadata_field_info=metadata_filed_info,
            document_contents=DOCUMENT_CONTENT_DESCRIPTION,
            verbose=verbose
        )
        response = query_retriever.invoke(query)
        if response == []:
            return "Sorry 🥲 we didnt the suitable MCP for your need"
        return response[0].page_content

    except Exception as error:
       print(f"Failed to generate content by self_query_retriever: {error}")

# if __name__ == '__main__':
#     query = "What is best MCP for prisma with more star"
#     print(self_query_retriever(query))
