from app.services.vector_store import vector_store
from langchain_groq import ChatGroq
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain.agents import create_agent
from langgraph.checkpoint.postgres import PostgresSaver
from collections.abc import Generator
from app.core.config import settings

# Initialize the Groq model
model = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model="llama-3.1-8b-instant",  # "openai/gpt-oss-20b"
    model_kwargs={"top_p": 0.9},
    temperature=0.2,
    max_tokens=512,
    timeout=60,
)


@dynamic_prompt
def prompt_with_context(request: ModelRequest) -> str:
    """Inject context into state messages."""
    last_query = request.state["messages"][-1].text
    retrieved_docs = vector_store.similarity_search(last_query, k=4)

    docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)

    system_message = f"""
        You are a legal assistant operating in a Retrieval-Augmented Generation (RAG) system.
        Your task is to answer user questions strictly based on the provided context.

        Rules:
        1. Use ONLY the information contained in context to generate your answer.
        2. Do NOT rely on general knowledge, assumptions, or external information.
        3. If the context does not contain sufficient or relevant information to answer the question, explicitly state that the information is not available in the provided documents.
        4. Do NOT fabricate legal facts, interpretations, or conclusions.
        5. Treat the context as excerpts from legal documents, regulations, court decisions, or authoritative legal commentary.
        6. Maintain a neutral, precise, and professional legal tone.

        Context: \n\n{docs_content}
    """

    return system_message


# def get_agent() -> Generator[PostgresSaver, None, None]:
#     """Create and return the RAG agent with Postgres checkpointer."""
#     with PostgresSaver.from_conn_string(
#         settings.SQLALCHEMY_DATABASE_URI
#     ) as checkpointer:
#         checkpointer.setup()  # auto create tables in PostgresSql
#         agent = create_agent(
#             model, tools=[], checkpointer=checkpointer, middleware=[prompt_with_context]
#         )
#         yield agent

agent = create_agent(model, tools=[], middleware=[prompt_with_context])
