from fastapi import APIRouter, Request
from app.schemas.agents import ChatMessage

router = APIRouter(prefix="/chat", tags=["agents"])


@router.post("", response_model=ChatMessage)
async def index(message: ChatMessage, request: Request) -> ChatMessage:
    # check message, apakah sudah ada thread_id
    # Jika sudah ada, maka gunakan thread_id tersebut
    # Jika belum ada, maka buat thread_id baru

    config = {"configurable": {"thread_id": "1"}}  # Dummy thread_id for example

    agent = request.app.state.agent
    ai_msg = await agent.ainvoke({"messages": [message.model_dump()]}, config=config)
    response = ai_msg["messages"][-1]
    return ChatMessage(role="assistant", content=response.content)
