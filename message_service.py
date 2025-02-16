from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

HASH_TABLE = {}

class MessageFedaultHandler(BaseModel):
    static_text: str


@app.get("/message_handler")
def handle() -> MessageFedaultHandler:
    """
    Returns a static text.
    """
    return {"static_text": "Not implemented yet"}

