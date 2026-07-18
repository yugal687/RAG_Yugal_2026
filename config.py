import os

from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("pcsk_5sLsPP_TR9RwaMWhFPDwCVRbjbXw6tJYRF8NyNiZYzRXrVJYLnPgzBsHvhFtmUQ2HTaBBu")

INDEX_NAME = "basic-rag"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100