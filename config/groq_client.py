from groq import Groq
import json
from config import EHANCE_DESCRIPTOIN_PROMPT, groq_api_key, DescriptionModel


class GroqClient:
    def __init__(self):
        self.client = Groq(api_key=groq_api_key)

    async def generate_content(self, contents:str):
        chat_completion = self.client.chat.completions.create(
            messages=[
                # Set an optional system message. This sets the behavior of the
                # assistant and can be used to provide specific instructions for
                # how it should behave throughout the conversation.
                {
                    "role": "system",
                    "content": f"{EHANCE_DESCRIPTOIN_PROMPT}"
                    f" YOU MUST USE JSON FILE {json.dumps(DescriptionModel.model_json_schema())}",
                },
                # Set a user message for the assistant to respond to.
                {
                    "role": "user",
                    "content": contents,
                }
            ],
            model="deepseek-r1-distill-llama-70b",
            temperature=0.1,
            max_completion_tokens=300,
            top_p=1,
            stop=None,
            stream=None,
            response_format={"type": "json_object"}
        )

        return chat_completion.choices[0].message.content