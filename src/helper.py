# src/preprocessing.py

import os
import re
import ast
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.embeddings import HuggingFaceEmbeddings

# Ensure NLTK resources are ready
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

# ---------- TEXT CLEANING ----------
lemmatizer = WordNetLemmatizer()

def clean_ingredients_column(value):
    """
    Cleans and lemmatizes ingredients column values.
    Example: ['Eggs', 'Tomatoes'] → 'egg tomato'
    """
    if isinstance(value, str):
        try:
            value = ast.literal_eval(value)
        except (ValueError, SyntaxError):
            value = [value]
    elif not isinstance(value, list):
        value = [str(value)]
    
    text = ' '.join(map(str, value)).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = ' '.join([lemmatizer.lemmatize(word) for word in text.split()])
    return text


def safely_eval_list(x):
    """
    Safely evaluates a stringified list (e.g. "['step1', 'step2']")
    and joins it into a single string.
    """
    if isinstance(x, str) and x.startswith('[') and x.endswith(']'):
        try:
            x = ast.literal_eval(x)
        except:
            x = [x]
    elif not isinstance(x, list):
        x = [str(x)]
    return ' '.join(x)


# ---------- CSV LOADING & COMBINATION ----------
def preprocess_recipes(input_path, output_path="data/recipes_for_embedding.csv"):
    """
    Loads raw recipe CSV, cleans and combines text columns.
    Saves the combined text to a new CSV for embedding.
    """
    df = pd.read_csv(input_path)
    
    # Clean ingredients & directions
    df["ingredients"] = df["ingredients"].apply(clean_ingredients_column)
    df["directions"] = df["directions"].apply(safely_eval_list)
    
    # Drop unnecessary columns
    df = df.drop(columns=["num_ingredients", "num_steps"], errors="ignore")
    
    # Combine relevant columns
    df["combined_text"] = (
        df["recipe_title"].astype(str) + " " +
        df["category"].astype(str) + " " +
        df["subcategory"].astype(str) + " " +
        df["description"].astype(str) + " " +
        df["ingredients"].astype(str) + " " +
        df["directions"].astype(str)
    )
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df[["combined_text"]].to_csv(output_path, index=False)
    print(f"✅ Combined text saved to {output_path}")
    return df


# ---------- CHUNKING ----------
def chunk_text(df, chunk_size=500, chunk_overlap=50, output_path="data/recipes_chunks.csv"):
    """
    Splits each combined recipe text into smaller chunks for embedding.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n", ".", "!", "?", ",", " ", ""]
    )

    chunks = []
    for i, row in df.iterrows():
        text = str(row["combined_text"]).strip()
        if text:
            splits = text_splitter.split_text(text)
            for j, chunk in enumerate(splits):
                chunks.append({
                    "recipe_id": i,
                    "chunk_id": j,
                    "text_chunk": chunk
                })
    
    chunks_df = pd.DataFrame(chunks)
    chunks_df.to_csv(output_path, index=False)
    print(f"✅ Chunking complete! Saved as {output_path}")
    return chunks_df


# ---------- DOCUMENT CONVERSION ----------
def create_documents(chunks_csv="data/recipes_chunks.csv"):
    """
    Converts the chunked CSV into LangChain Document objects.
    """
    df = pd.read_csv(chunks_csv)
    documents = [
        Document(
            page_content=row["text_chunk"],
            metadata={"recipe_id": row["recipe_id"], "chunk_id": row["chunk_id"]}
        )
        for _, row in df.iterrows()
    ]
    print(f"✅ Loaded {len(documents)} documents.")
    return documents


# ---------- EMBEDDINGS ----------
def download_embeddings():
    """
    Loads HuggingFace MiniLM embeddings (384D).
    """
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    print("✅ HuggingFace embeddings model loaded.")
    return embeddings


# ---------- RUN FULL PIPELINE ----------
if __name__ == "__main__":
    input_csv = "data/1_Recipe_csv.csv"
    df = preprocess_recipes(input_csv)
    chunks_df = chunk_text(df)
    docs = create_documents()
    embedding_model = download_embeddings()