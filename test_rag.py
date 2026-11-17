
from rag import process_pdf, ask_pdf_question
from chatbot import get_pdf_response

# Get PDF file path
file_path = input("Enter your PDF file path: ").strip().strip('"')

# Process PDF
with open(file_path, "rb") as pdf_file:

    index, chunks, message = process_pdf(pdf_file)

print("\n", message)

if index is not None:

    print("Total chunks created:", len(chunks))

    # Ask a question
    question = input("\nAsk a question about your PDF: ")

    # Retrieve relevant information
    relevant_context = ask_pdf_question(
        question,
        index,
        chunks
    )

    # Generate AI answer
    answer = get_pdf_response(
        question,
        relevant_context
    )

    print("\nAI ANSWER:")
    print("--------------------------------")
    print(answer)
