import os
from dotenv import load_dotenv

from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# Load env variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")

# Embedding model
embedding_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# Vector store initialization (persistent)
def get_vectorstore():
    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_model
    )

# Load and split document
def process_document(file_path: str):
    loader = TextLoader(file_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)

    vectorstore = get_vectorstore()
    vectorstore.add_documents(chunks)
    vectorstore.persist()

    return {"chunks": len(chunks), "path": file_path}

# Run a RAG query
def run_query(question: str) -> str:
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever()

    llm = ChatOpenAI(temperature=0.2, openai_api_key=OPENAI_API_KEY)
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False
    )
    result = qa.run(question)
    return result
