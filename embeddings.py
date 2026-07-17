from sentence_transformers import SentenceTransformer

# Load the model once when the file is imported

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def create_embeddings(texts):

    """

    Convert a list of text chunks into embedding vectors.

    """

    return embedding_model.encode(texts)