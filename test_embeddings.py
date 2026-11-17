
from embedding_model import generate_embeddings

# Sample text chunks
chunks = [
    "Artificial Intelligence allows machines to perform intelligent tasks.",
    "Machine Learning is a subset of Artificial Intelligence.",
    "Python is a popular programming language."
]

# Generate embeddings
embeddings = generate_embeddings(chunks)

# Display results
print("Embeddings generated successfully!")

print("Number of chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)

print("\nFirst embedding:")
print(embeddings[0])
