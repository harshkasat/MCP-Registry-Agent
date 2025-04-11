import json
from typing import Dict, Any
from langchain_text_splitters import RecursiveJsonSplitter
from langchain_experimental.text_splitter import SemanticChunker
from config.google_gemini import LangchainGeminiClient


def _json_text_splitter(converted_dict: Dict[str, Any]):
    try:
        splitter = RecursiveJsonSplitter(max_chunk_size=768)
        json_chunks = splitter.split_json(json_data=converted_dict)
        text_chunks = splitter.split_text(json_data=converted_dict)
        print("@@TEXT CHUNKS ", type(text_chunks))
        print("@@JSON CHUNKS ", type(json_chunks))
        # print("@@CONVERT DICT ", converted_dict)

        # return text_chunks
        return json_chunks
    except Exception as error:
        print(f"Failed to split text by _json_text_splitter: {error}")

def _semantic_chunker():
    try:
        gemini_embedd = LangchainGeminiClient().generate_embeddings()
        text_splitter = SemanticChunker(gemini_embedd, breakpoint_threshold_type='percentile', breakpoint_threshold_amount=90) # choose which embeddings and breakpoint type and threshold to use
        return text_splitter
    except Exception as error:
        print(f"Failed to split text by _semantic_chunker: {error}")

# if __name__ == '__main__':
#     with open('all_mcp_server.json', 'r', encoding='utf-16') as file:
#             json_data = json.load(file)
#     converted_dict = {item["title"]: item['description'] for item in json_data}
#     print(_json_text_splitter(converted_dict=converted_dict))
#     # _json_text_splitter()