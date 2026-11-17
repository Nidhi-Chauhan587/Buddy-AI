
from chatbot import get_response

print("Buddy AI - Your Friendly AI Companion")
print("--------------------")

question = input("You: ")

answer = get_response(question)

print("\nAI:", answer)
