import os
from pydantic import BaseModel
from enum import Enum
from dotenv import load_dotenv
load_dotenv()

MCP_INTRO = "MCP is an open protocol that standardizes how applications provide context to LLMs." \
"Think of MCP like a USB-C port for AI applications. Just as USB-C provides a standardized way to connect your" \
"devices to various peripherals and accessories, MCP provides a standardized way to connect AI models to different data sources and tools." \
"Why MCP?" \
"MCP helps you build agents and complex workflows on top of LLMs. LLMs frequently need to integrate with data and tools, and MCP provides:" \
"A growing list of pre-built integrations that your LLM can directly plug into" \
"The flexibility to switch between LLM providers and vendors" \
"Best practices for securing your data within your infrastructure" \

EHANCE_DESCRIPTOIN_PROMPT = "You are a helpful assistant that writes engaging and " \
f"informative descriptions for open-source Model Context Protcol, here quick intro about MCP: {MCP_INTRO}. " \
"Given the following data about an MCP server, create a detailed project description " \
"suitable for a GitHub README or website landing page. Make sure the tone is friendly, " \
"informative, and developer-focused. Highlight what the project does, who made it, " \
"what makes it special, its technical foundation, and the popularity (like GitHub stars)."


class DescriptionModel(BaseModel):
    description:str


class TaskTypeEnum(str, Enum):
    RETRIEVAL_QUERY = "retrieval_query"
    RETRIEVAL_DOCUMENT = "retrieval_document"
    SEMANTIC_SIMILARITY = "semantic_similarity"
    CLASSIFICATION = "classification"
    CLUSTERING = "clustering"

SAFE_SETTINGS = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

genai_api_key = os.getenv('GEMINI_API_KEY')
os.environ['GOOGLE_API_KEY'] = os.getenv('GEMINI_API_KEY')
if genai_api_key is None:
    raise ValueError("Missing GEMINI_API_KEY environment variable")

groq_api_key = os.getenv('GROQ_API_KEY')
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
if groq_api_key is None:
    raise ValueError("Missing GROQ API KEY enviroment variable")
