
import os
from dotenv import load_dotenv
from groq import Groq

# Load API key
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("Groq API key not found in .env")

# Connect to Groq
client = Groq(api_key=api_key)

print("Testing Groq AI...")
print("--------------------")

try:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": "Explain Artificial Intelligence in simple words."
            }
        ]
    )

    print("\nGroq AI Response:")
    print(response.choices[0].message.content)

except Exception as e:
    print("\nGroq Error:", e)
