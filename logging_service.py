from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

class MessageRequestQuery(BaseModel):
    UUID: str
    msg: str

class MessageResponseQuery(BaseModel):
    msgs: str


HASH_TABLE = {}


@app.post("/fetching_message")
def fulfill_hash_table(query: MessageRequestQuery) -> Dict[str, str]:
    """
    Saves messages to the Hash Table with key as uuid and value -- message.

    Args:
        query (.UUID (str)) -- unique identificator of message.
        query (.msg (str)) -- message from the client.
    Returns:
        {"status": "ok"} 
    Prints: 
        Message that was saved.
        Example: "Saved message: Hello"
    """
    unique_id = query.UUID
    message = query.msg

    if unique_id in HASH_TABLE:
        return {"status": "duplicate, ok"}

    HASH_TABLE[unique_id] = message
    print("Saved message: ", message)

    return {"status": "ok"} 


@app.get("/get_fetched_messages")
def get_fetched_messages() -> MessageResponseQuery:
    """
    Returns all messages from the Hash Table.

    Args:
        None
    Returns:
        {"msgs": "<all messages separated by ', '>"}
    """
    return {"msgs": ", ".join(list(HASH_TABLE.values()))}
