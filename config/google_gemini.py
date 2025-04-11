from google import genai
import asyncio
from google.genai import types
from config import genai_api_key, SAFE_SETTINGS, EXTRACT_DESCRIPTOIN_PROMPT, DescriptionModel
from pydantic import BaseModel



# Initialize the API client
class GeminiClient():

    def __init__(self):
        self.configure_llm = genai.Client(api_key=genai_api_key)


    async def generate_content(self, contents:str):
        try:
            llm = self.configure_llm
            response = llm.models.generate_content(
                model="gemini-2.0-flash",
                config=types.GenerateContentConfig(
                    system_instruction=EXTRACT_DESCRIPTOIN_PROMPT,
                    safety_settings=SAFE_SETTINGS,
                    temperature=0.1,
                    response_mime_type='application/json',
                    response_schema=DescriptionModel
                ),
                contents=f"Here's the data: {contents}."
            )
            if response is None:
                return contents
            return response.text
        except Exception as e:
            print(f"Failed to generate content by GeminiClient().generate: {e}")
            return None

# if __name__ == '__main__':
#     content = {
#     "title": "cursor-rust-tools",
#     "link": "https://www.mcpserverfinder.com/servers/terhechte/cursor-rust-tools",
#     "created_by": "by terhechte",
#     "description": "A MCP server to allow the LLM in Cursor to access Rust Analyzer, Crate Docs and Cargo Commands.",
#     "stars": "616",
#     "categories": [
#       "mcp",
#       "mcp-server",
#       "mcp-tools",
#       "llm",
#       "cline",
#       "copilot",
#       "neovim"
#     ],
#     "language": "language",
#     "github_link": "https://github.com/terhechte/cursor-rust-tools?ref=mcpserverfinder.com"
#   }
#     # print("MCP CONTEXT", EXTRACT_DESCRIPTOIN_PROMPT)
#     response =asyncio.run(GeminiClient().generate_content(
#         contents=content))
#     print(response)
