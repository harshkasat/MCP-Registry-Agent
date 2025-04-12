from langchain.chains.query_constructor.schema import AttributeInfo

metadata_filed_info = [
    AttributeInfo(
        name="title",
        description="The name of the MCP-related title, "
        "often indicating its core functionality.",
        type="string"
    ),
    AttributeInfo(
        name="link",
        description="The URL to the tool or server's dedicated page on MCPServerFinder, where more information can be accessed.",
        type="string"
    ),
    AttributeInfo(
        name="created_by",
        description="The creator or maintainer of the tool or project, usually identified by username or alias.",
        type="string"
    ),
    AttributeInfo(
        name="stars",
        description="The number of GitHub stars the project has received, reflecting its popularity or credibility.",
        type="string"
    ),
    AttributeInfo(
        name="categories",
        description="A list of tags describing the tool's domain, including MCP relevance, usage context, programming environment, or integrations.",
        type="List[string]"
    ),
    AttributeInfo(
        name="language",
        description="The primary programming language used in the tool or project.",
        type="string"
    ),
    AttributeInfo(
        name="github_link",
        description="Direct link to the GitHub repository containing the tool's source code.",
        type="string"
    ),
]
