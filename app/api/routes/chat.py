from fastapi import APIRouter
from app.schemas.agents import ChatMessage
from app.services.rag_chains import agent

router = APIRouter(prefix="/chat", tags=["agents"])


@router.post("", response_model=ChatMessage)
def index(message: ChatMessage) -> ChatMessage:
    ai_msg = agent.invoke({"messages": [message.model_dump()]})
    response = ai_msg["messages"][-1]
    return ChatMessage(role="assistant", content=response.content)
