
import os
import re
from dotenv import load_dotenv
from google import genai
from groq import Groq
from search import search_web
from math_tool import calculate


load_dotenv()

import streamlit as st

try:
    GEMINI_API_KEY = st.secrets.get(
        "GEMINI_API_KEY",
        os.getenv("GEMINI_API_KEY")
    )
    GROQ_API_KEY = st.secrets.get(
        "GROQ_API_KEY",
        os.getenv("GROQ_API_KEY")
    )
except Exception:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# Connect to Gemini
gemini_client = None

if GEMINI_API_KEY:
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)


# Connect to Groq
groq_client = None

if GROQ_API_KEY:
    groq_client = Groq(api_key=GROQ_API_KEY)


# Instructions for both AI providers
SYSTEM_PROMPT = """
You are a smart, friendly and helpful AI assistant.

Follow these rules:
1. Explain concepts in simple and easy English.
2. Give step-by-step explanations for difficult topics.
3. For coding questions, provide correct code with explanations.
4. Use examples wherever they help understanding.
5. Keep answers clear, organized and relevant.
6. Avoid unnecessary technical terms when explaining to beginners.
7. Use previous conversation context for follow-up questions.
8. If you are unsure about something, say so honestly.
9. Do not make up facts or information.
10. Be polite, supportive and professional.
11. For current news, latest updates, or changing information, use the provided web search results.
12. Clearly distinguish information found through web search from general knowledge.
13. Never invent search results, sources, or website links.
"""


# Detect basic mathematical expressions
def is_math_question(question):

    question = question.lower().strip()

    math_keywords = [
        "calculate",
        "solve",
        "square root",
        "multiply",
        "divide",
        "addition",
        "subtraction"
    ]

    if any(keyword in question for keyword in math_keywords):
        return True

    # Detect expressions such as 25 * 48 or 100 / 5
    expression_pattern = r"\d+\s*[\+\-\*/\^%]\s*\d+"

    return bool(re.search(expression_pattern, question))


# Main chatbot response function
def get_response(chat_history):

    # Support both a single question and conversation history
    if isinstance(chat_history, str):
        chat_history = [
            {"role": "user", "content": chat_history}
        ]

    # Prepare conversation for Gemini
    conversation = ""

    for message in chat_history:

        role = message["role"]
        content = message["content"]

        if role == "user":
            conversation += "User: " + content + "\n"

        elif role == "assistant":
            conversation += "Assistant: " + content + "\n"

    conversation += "Assistant:"

    # Find the latest user question
    last_user_query = ""

    for message in reversed(chat_history):

        if message["role"] == "user":
            last_user_query = message["content"]
            break

    # Check whether the question is mathematical
    if is_math_question(last_user_query):

        math_result = calculate(last_user_query)

        if "could not calculate" not in math_result.lower():
            return (
                "The calculated answer is: **"
                + math_result
                + "**"
            )

    # Check whether internet search is needed
    search_context = ""

    search_keywords = [
        "latest", "current", "today", "recent",
        "news", "updates", "2026", "price",
        "who is the current", "what happened"
    ]

    if any(
        word in last_user_query.lower()
        for word in search_keywords
    ):

        print("Searching the internet...")

        results = search_web(last_user_query)

        if results:

            search_context = "\n\nWeb Search Results:\n"

            for result in results:

                search_context += (
                    "\nTitle: " + result["title"] +
                    "\nDescription: " + result["body"] +
                    "\nSource: " + result["url"] +
                    "\n"
                )

        else:

            search_context = (
                "\nNo web search results were found. "
                "Do not invent current information."
            )

    # STEP 1: Try Gemini first
    if gemini_client:

        try:

            response = gemini_client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=(
                    SYSTEM_PROMPT
                    + "\n\nConversation:\n"
                    + conversation
                    + search_context
                )
            )

            if response.text:

                print("Response generated using Gemini.")
                return response.text

        except Exception as e:

            print("Gemini failed:", e)

    # STEP 2: If Gemini fails, try Groq
    if groq_client:

        try:

            messages = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT + "\n\n" + search_context
                }
            ]

            for message in chat_history:

                if message["role"] in ["user", "assistant"]:

                    messages.append({
                        "role": message["role"],
                        "content": message["content"]
                    })

            response = groq_client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=messages
            )

            answer = response.choices[0].message.content

            if answer:

                print("Response generated using Groq.")
                return answer

        except Exception as e:

            print("Groq failed:", e)

    # STEP 3: If both providers fail
    return (
        "Sorry, both AI services are temporarily unavailable. "
        "Please try again later."
    )


# PDF question-answering function
def get_pdf_response(question, relevant_context):

    prompt = f"""
You are a helpful AI assistant answering questions
about an uploaded PDF.

Answer the user's question using the PDF information
provided below.

Instructions:
1. Use the PDF context as your main source.
2. Explain the answer in simple English.
3. Give examples wherever useful.
4. If the answer is not available in the PDF,
   clearly say that it was not found in the document.
5. Do not invent information.

PDF INFORMATION:
{relevant_context}

USER QUESTION:
{question}

Provide a clear and helpful answer:
"""

    # Try Gemini first
    if gemini_client:

        try:

            response = gemini_client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

            if response.text:

                print("PDF answer generated using Gemini.")
                return response.text

        except Exception as e:

            print("Gemini PDF response failed:", e)

    # Try Groq if Gemini fails
    if groq_client:

        try:

            response = groq_client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "system",
                        "content": "You answer questions using only the supplied PDF context."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            answer = response.choices[0].message.content

            if answer:

                print("PDF answer generated using Groq.")
                return answer

        except Exception as e:

            print("Groq PDF response failed:", e)

    return "Sorry, both AI services are currently unavailable."
