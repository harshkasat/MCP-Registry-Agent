import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import asyncio
from config.google_gemini import GeminiClient
from config.groq_client import GroqClient


BATCH_SIZE = 15
DELAY_SECONDS = 30

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

    updated_descriptions = []
    idx = 0

    descriptions_to_update = [item['description'] for item in data if 'description' in item]
    
    for i in range(0, len(descriptions_to_update), BATCH_SIZE):
        batch = descriptions_to_update[i:i+BATCH_SIZE]

        # enhance_mcp_description_groq(item['description']) --> Alternative GROQ API
        tasks = [enhance_mcp_description_gemini(desc) for desc in batch]
        results = await asyncio.gather(*tasks)

        updated_descriptions.extend(results)

        if i + BATCH_SIZE < len(descriptions_to_update):
            print(f"⏳ Sleeping for {DELAY_SECONDS} seconds after batch {i//BATCH_SIZE + 1}")
            await asyncio.sleep(DELAY_SECONDS)

    # Update descriptions in the original data
    for item in data:
        if 'description' in item:
            updated = json.loads(updated_descriptions[idx])
            item['description'] = updated['description']
            idx += 1

    # Save updated data
    with open('all_mcp_server.json', 'w', encoding='utf-16') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    print(f"\n✅ Successfully updated and saved {idx} descriptions.")

if __name__ == "__main__":
    import time
    start = time.time()
    asyncio.run(enhance_mcp_description())
    print("Total Time Taken to completed: ", time.time() - start)