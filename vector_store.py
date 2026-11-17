
import faiss
import numpy as np


def create_vector_store(embeddings):

    # Get embedding dimensions
    dimension = embeddings.shape[1]

    # Create FAISS index
    index = faiss.IndexFlatL2(dimension)

    # Convert embeddings into float32
    embeddings = np.array(
        embeddings,
        dtype=np.float32
    )

    # Store embeddings in FAISS
    index.add(embeddings)

    return index


def search_vectors(index, query_embedding, top_k=3):

    # Convert query embedding into float32
    query_embedding = np.array(
        [query_embedding],
        dtype=np.float32
    )

    # Search for similar vectors
    distances, indices = index.search(
        query_embedding,
        top_k
    )

    return distances, indices
