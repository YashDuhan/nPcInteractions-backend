from fastapi import APIRouter
from .endpoints import chat_ankit, chat_aman, chat_aakash

app_router = APIRouter()

app_router.post("/chat-ankit")(chat_ankit)

app_router.post("/chat-aman")(chat_aman)

app_router.post("/chat-aakash")(chat_aakash)
