
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("Groq API key not found!")
else:
    client = Groq(api_key=api_key)

    try:
        models = client.models.list()

        print("Models available to your Groq account:")
        print("----------------------------------------")

        for model in models.data:
            print(model.id)

    except Exception as e:
        print("Error:", e)
