from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

response = client.responses.create(
    model="gpt-4.1-nano",
    instructions="Talk like a pirate.",
    input="Are semicolens optional in JavaScript?",
)

print(response.output_text)
