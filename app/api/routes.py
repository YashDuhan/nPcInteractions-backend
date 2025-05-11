from fastapi import APIRouter
from .endpoints import chat_ankit, chat_aman, chat_aakash

app_router = APIRouter()

app_router.get("/chat-ankit")(chat_ankit)

app_router.get("/chat-aman")(chat_aman)

app_router.get("/chat-aakash")(chat_aakash)
