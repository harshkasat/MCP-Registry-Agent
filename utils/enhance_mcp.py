import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import asyncio
from config.google_gemini import GeminiClient
from config.groq_client import GroqClient

async def enhance_mcp_description_gemini(old_description: str):
    try:
        update_description = await GeminiClient().generate_content(contents=old_description)
        return update_description
    except Exception as error:
        print(f"When running enhance_mcp_description_gemini we got this error: {error}")
        return old_description  # fallback to original if error

async def enhance_mcp_description_groq(old_description: str):
    try:
        update_description = await GroqClient().generate_content(contents=old_description)
        print(update_description)
        return update_description
    except Exception as error:
        print(f"When running enhance_mcp_description_groq we got this error: {error}")
        return old_description

async def enhance_mcp_description():
    # Load JSON data
    with open('all_mcp_server.json', 'r', encoding='utf-16') as file:
        data = json.load(file)

    # Prepare async enhancement tasks
    tasks = [
        enhance_mcp_description_gemini(item['description'])
        # enhance_mcp_description_groq(item['description'])  # use this instead if needed
        for item in data if 'description' in item
    ]

    # Await all tasks
    updated_descriptions = await asyncio.gather(*tasks)

    # Update descriptions in the original data
    idx = 0
    for item in data:
        if 'description' in item:
            item['description'] = json.loads(updated_descriptions[idx])['description']
            # temp = json.loads(updated_descriptions[idx])
            # print("@@ID", idx)
            # print(temp['description'])
            idx += 1

    # Save updated data back to the same file
    with open('all_mcp_server.json', 'w', encoding='utf-16') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    print(f"\n✅ Successfully updated and saved {idx} descriptions.")

if __name__ == "__main__":
    asyncio.run(enhance_mcp_description())
