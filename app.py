from flask import Flask, render_template, jsonify, request
from src.helper import (
    preprocess_recipes,
    chunk_text,
    create_documents,
    download_embeddings
)
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
from langchain.chains import RetrievalQA
from src.prompt import *

app = Flask(__name__)
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

embeddings = download_embeddings()

index_name = "cooking-assistant" 
# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)


retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 5})

# initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.3
)


rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)





@app.route('/')
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    print("User message:", msg)

    try:
        response = rag_chain.invoke({"query": msg})
        print("Raw RAG response:", response)
        answer = response.get("result", "⚠️ No valid response.")
        return str(answer)
    except Exception as e:
        print("🔥 Error occurred:", e)
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host="0.0.0.0",port= 8080,debug=True)

    