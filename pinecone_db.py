import os
from pinecone import Pinecone, ServerlessSpec
from config import PINECONE_API_KEY, INDEX_NAME

pc = Pinecone(api_key=PINECONE_API_KEY)

def get_index():
    # Get existing index names
    existing_indexes = [index.name for index in pc.list_indexes()]
    # Create the index if it doesn't exist
    if INDEX_NAME not in existing_indexes:
        print(f"Creating index '{INDEX_NAME}'...")
        pc.create_index(
            name=INDEX_NAME,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        print("Index created successfully.")
    else:
        print(f"Index '{INDEX_NAME}' already exists.")
    return pc.Index(INDEX_NAME)

#uploaded one chuck for test
# def upload_one_chunk(index, chunk, embedding):
#     vector = {
#         "id": "chunk_0",
#         "values": embedding.tolist(),
#         "metadata": {
#             "text": chunk
#         }
#     }
#     index.upsert(vectors=[vector])
#     print("Uploaded one vector!")

def upload_chunks(index, chunks, embeddings, source):
    vectors = []
    document_name = os.path.splitext(source)[0]  # Get the document name without extension
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        vectors.append({
            "id": f"{document_name}_chunk_{i}",
            "values": embedding.tolist(),
            "metadata": {
                "text": chunk,
                "source": source,
                "chunk_number": i
            }
        })
    index.upsert(vectors=vectors)
    print(f"Uploaded {len(vectors)} chunks from {source}.")