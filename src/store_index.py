import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

# Import all helper functions
from helper import (
    preprocess_recipes,
    chunk_text,
    create_documents,
    download_embeddings
)

# ---------- Initialize Pinecone ----------
def initialize_pinecone():
    load_dotenv()

    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

    pc = Pinecone(api_key=PINECONE_API_KEY)
    index_name = "cooking-assistant"

    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            dimension=384,  # embedding size for MiniLM
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        print(f"✅ Created new Pinecone index: {index_name}")
    else:
        print(f"✅ Using existing Pinecone index: {index_name}")

    return index_name, pc


# ---------- Store Embeddings ----------
def store_embeddings(chunks_csv_path="data/recipes_chunks.csv"):
    documents = create_documents(chunks_csv_path)
    embedding_model = download_embeddings()
    index_name, pc = initialize_pinecone()

    PineconeVectorStore.from_documents(
        documents=documents,
        embedding=embedding_model,
        index_name=index_name
    )
    print("✅ All embeddings successfully stored in Pinecone!")


# ---------- Full Automation ----------
if __name__ == "__main__":
    input_csv = "data/1_Recipe_csv.csv"
    chunks_csv_path = "data/recipes_chunks.csv"

    print("🚀 Starting preprocessing pipeline...")

    # Step 1: Clean + combine text
    df = preprocess_recipes(input_csv)

    # Step 2: Chunk data
    chunk_text(df, output_path=chunks_csv_path)

    # Step 3: Create index and upload embeddings
    store_embeddings(chunks_csv_path)

    print("🎉 Pipeline completed! Pinecone index is ready.")