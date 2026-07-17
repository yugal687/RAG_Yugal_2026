from embeddings import create_embeddings


def retrieve(index, question, top_k=3):
    """
    Search Pinecone for the most relevant chunks.
    """

    # Convert question into an embedding
    question_embedding = create_embeddings([question])[0]

    # Search Pinecone
    results = index.query(
        vector=question_embedding.tolist(),
        top_k=top_k,
        include_metadata=True
    )

    return results