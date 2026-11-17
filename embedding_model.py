
from sentence_transformers import SentenceTransformer

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(text_chunks):

    embeddings = model.encode(
        text_chunks,
        convert_to_numpy=True
    )

    return embeddings
