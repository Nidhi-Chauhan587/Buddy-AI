
from pdf_reader import extract_text_from_pdf
from text_chunker import split_text
from embedding_model import generate_embeddings
from vector_store import create_vector_store, search_vectors


def process_pdf(pdf_file):

    # Step 1: Extract PDF text
    text = extract_text_from_pdf(pdf_file)

    if not text or not text.strip():
        return None, None, "Could not extract readable text from PDF."

    if text.startswith("Error reading PDF:") or text.startswith("No readable text"):
        return None, None, "Could not extract readable text from PDF."

    # Step 2: Split text into chunks
    chunks = split_text(text)

    if not chunks:
        return None, None, "No text chunks were created."

    # Step 3: Generate embeddings
    embeddings = generate_embeddings(chunks)

    # Step 4: Create FAISS vector database
    index = create_vector_store(embeddings)

    return index, chunks, "PDF processed successfully!"


def ask_pdf_question(question, index, chunks):

    # Check question
    if not question or not question.strip():
        return ""

    # Generate question embedding
    query_embedding = generate_embeddings([question])

    # Retrieve relevant chunks
    distances, indices = search_vectors(
        index,
        query_embedding[0],
        top_k=min(3, len(chunks))
    )

    # Collect relevant text
    relevant_text = []

    for i in indices[0]:

        if 0 <= i < len(chunks):
            if chunks[i] and chunks[i].strip():
                relevant_text.append(chunks[i])

    return "\n\n".join(relevant_text)
