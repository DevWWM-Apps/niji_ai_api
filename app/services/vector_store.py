from langchain_postgres import PGVector
from langchain_huggingface import HuggingFaceEmbeddings
from app.core.config import settings

embeddings = HuggingFaceEmbeddings(
    model="BAAI/bge-m3",
    model_kwargs={"device": "cuda"},
    encode_kwargs={"normalize_embeddings": True},
)

vector_store = PGVector(
    embeddings=embeddings,
    collection_name="law_journals",
    connection=settings.SQLALCHEMY_DATABASE_URI,
    use_jsonb=True,
)
