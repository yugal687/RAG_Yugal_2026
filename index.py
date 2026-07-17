from pdf_loader import load_pdf
from chunker import chunk_text
from embeddings import create_embeddings
from pinecone_db import get_index, upload_chunks


def index_documents():

    text = load_pdf("data/document.pdf")

    chunks = chunk_text(text)

    embeddings = create_embeddings(chunks)

    index = get_index()

    upload_chunks(
        index,
        chunks,
        embeddings
    )

    print(index.describe_index_stats())


if __name__ == "__main__":
    index_documents()