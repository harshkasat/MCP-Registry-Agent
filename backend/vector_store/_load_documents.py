import json
from config.google_gemini import LangchainGeminiClient
from langchain_core.documents import Document

# from utils.docs_text_splitter import _json_text_splitter, _semantic_chunker, LangchainGeminiClient
# from config.google_gemini import LangchainGeminiClient



def create_vector_store_document():

    with open('all_mcp_server.json', 'r', encoding='utf-16') as file:
        json_data = json.load(file)
    # converted_dict = {item["title"]: item['description'] for item in json_data}
    total_documents = []
    for item in json_data:
        total_documents.append(
            Document(
                page_content=item['description'],
               metadata = {
                    "title": item.get('title', '') or '',
                    "link": item.get('link', '') or '',
                    "created_by": item.get('created_by', '') or '',
                    "stars": item.get('stars', 0) or 0,
                    "categories": item.get('categories', []) or [],
                    "language": item.get('language', '') or '',
                    "github_link": item.get('github_link', '') or '',
                }

            )
        )
    # uuids = [str(uuid4()) for _ in range(len(total_documents))]
    # vector_store.add_documents(documents=total_documents, ids=uuids)
    return total_documents

# if __name__ == '__main__':
#     import asyncio
#     asyncio.run(create_vector_store_document())
