
from text_chunker import split_text

# Sample text for testing
text = """
Artificial Intelligence is a branch of computer science.
Machine Learning is a subset of Artificial Intelligence.
Deep Learning is a subset of Machine Learning.
Natural Language Processing helps computers understand human language.
"""

# Divide text into chunks
chunks = split_text(
    text,
    chunk_size=100,
    overlap=20
)

# Display results
print("Total chunks created:", len(chunks))

for i, chunk in enumerate(chunks, start=1):
    print(f"\nChunk {i}:")
    print(chunk)
