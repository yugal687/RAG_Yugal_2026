import os

from pdf_loader import load_pdf
from chunker import chunk_text
from embeddings import create_embeddings
from pinecone_db import get_index, upload_chunks
from config import CHUNK_SIZE, CHUNK_OVERLAP


DATA_FOLDER = "data"


def index_documents():

    index = get_index()

    for filename in os.listdir(DATA_FOLDER):

        if not filename.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(DATA_FOLDER, filename)

        print(f"\nIndexing: {filename}")

        text = load_pdf(pdf_path)

        chunks = chunk_text(text, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

        embeddings = create_embeddings(chunks)

        upload_chunks(
            index=index,
            chunks=chunks,
            embeddings=embeddings,
            source=filename
        )

    print("\nIndexing Complete!")
    print(index.describe_index_stats())


if __name__ == "__main__":
    index_documents()