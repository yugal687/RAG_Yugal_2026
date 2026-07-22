# {
#  "cells": [
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "pip install langchain langchain-community chromadb sentence-transformers ollama"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {},
#    "outputs": [],
#    "source": []
#   }
#  ],
#  "metadata": {
#   "kernelspec": {
#    "display_name": "Python 3",
#    "language": "python",
#    "name": "python3"
#   },
#   "language_info": {
#    "name": "python",
#    "version": "3.12.8"
#   }
#  },
#  "nbformat": 4,
#  "nbformat_minor": 2
# }



from pdf_loader import load_pdf
from chunker import chunk_text
from embeddings import create_embeddings
from pinecone_db import get_index
from pinecone_db import upload_chunks
from retriever import retrieve

text = load_pdf("data/document.pdf")

chunks = chunk_text(text)

print(f"Total Chunks: {len(chunks)}")

for i, chunk in enumerate(chunks):
    print("=" * 60)
    print(f"Chunk {i+1}")
    print("=" * 60)
    print(chunk)
    print()

#embedding creation
embeddings = create_embeddings(chunks)

print(f"Embedding Shape: {embeddings.shape}")

index = get_index()

print("Connected to Pinecone!")

print(index.describe_index_stats())

# upload_chunks(
#     index,
#     chunks,
#     embeddings
# )
upload_chunks(
    index=index,
    chunks=chunks,
    embeddings=embeddings,
    source="document.pdf"
)

print(index.describe_index_stats())

question = "Who unified Nepal?"

results = retrieve(index, question)

contexts = []

for match in results["matches"]:

    contexts.append(match["metadata"]["text"])

context = "\n\n".join(contexts)

print(context)

print("\nRetrieved Chunks:\n")

for match in results["matches"]:
    print("=" * 60)
    print(f"Score: {match['score']:.4f}")
    print(match["metadata"]["text"])
    print()
    