
from embedding_model import generate_embeddings
from vector_store import create_vector_store, search_vectors

# Sample text chunks
chunks = [
    "Artificial Intelligence allows machines to perform intelligent tasks.",
    "Machine Learning is a subset of Artificial Intelligence.",
    "Python is a popular programming language."
]

# Generate embeddings
embeddings = generate_embeddings(chunks)

# Create FAISS database
index = create_vector_store(embeddings)

print("FAISS vector database created!")
print("Total vectors stored:", index.ntotal)

# Search using a question
question = "What is Machine Learning?"

query_embedding = generate_embeddings([question])

distances, indices = search_vectors(
    index,
    query_embedding[0],
    top_k=2
)

print("\nRelevant chunks:")

for i in indices[0]:
    print("-", chunks[i])
