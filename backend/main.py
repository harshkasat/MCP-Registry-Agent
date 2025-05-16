from mcp_manage.servers.sse_server.terminal_server_sse import uvicorn_server
# from vector_store._load_documents import create_vector_store_document
# from vector_store.manage_vector_store import PineconeVectorStoreManage
# from config.google_gemini import LangchainGeminiClient


# def main():
#     # embeddings = LangchainGeminiClient().generate_embeddings()
#     # documents = create_vector_store_document()
#     vector_store = PineconeVectorStoreManage()
#     # doc_search = vector_store.create_documents(
#     #     documents=documents,
#     #     embeddings=embeddings
#     # )
#     print(vector_store.retrieve_query(
#         "What is best MCP for run prisma usin typescript for data management"
#     ))

if __name__ == '__main__':
    try:
        uvicorn_server()
    except Exception as error:
        print(f" When running the MCP SSE using uvicorn {error}")
        raise
