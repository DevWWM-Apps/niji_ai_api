from langchain_community.document_loaders import DirectoryLoader
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.services.vector_store import vector_store

# Document Loading
loader = DirectoryLoader(path="../data/raw", glob="*.pdf", loader_cls=PyMuPDF4LLMLoader)
docs = loader.load()

# Text Splitting
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # 1500 1800 chunk size (characters)
    chunk_overlap=120,  # 200 250 chunk overlap (characters)
    add_start_index=True,  # track index in original document
    separators=["\n\n", "\n", " ", ""],
)
all_splits = text_splitter.split_documents(docs)

# Vector Store Ingestion
document_ids = vector_store.add_documents(documents=all_splits)
print(document_ids[:3])
