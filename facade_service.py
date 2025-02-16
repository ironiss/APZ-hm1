import uuid
import httpx
import asyncio
import logging

from config import LOGGINING_SERVICE_DOCKER, MESSAGES_SERVICE_DOCKER
from typing import Dict, Union

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class MessageRequestQuery(BaseModel):
    msg: str

class MessageResponseQuery(BaseModel):
    all_msgs: str


@app.post("/send_to_logging_service")
async def generate_uuid(query: MessageRequestQuery) -> Dict[str, str]: 
    """
    Generating UUID for message and sending to the logging-service.
    HTTP POST to the loggining service with query: {UUID (str), msg(str)}

    Args:
        query (.msg (str)) -- message from the client
    Returns:
        {"status": "<status code>"}
    """

    unique_id = str(uuid.uuid4())
    data_query = {"UUID": unique_id, "msg": query.msg}

    async with httpx.AsyncClient() as client:
        for num in range(5):
            try:
                response = await client.post(url=LOGGINING_SERVICE_DOCKER+"/fetching_message", json=data_query, headers = {"Content-Type": "application/json"})

                if response.status_code == 200:
                    logging.info(f"Try number {num} is successful")
                    return {"status": str(response.status_code)}
                
            except httpx.RequestError as e:
                logging.info(f"Try number {num}, error: {str(e)}")
                await asyncio.sleep(10)

    # requests.post(url=MESSAGES_SERVICE+"/message_handler")
    return {"status": "500"}


  
@app.get("/get_resulted_messages")
async def get_messages() -> Union[MessageResponseQuery, Dict[str, str]]:
    """
    Gets all messages that was saved by logging-service.

    Args:
        None
    Returns:
        {"all_msgs": "<all messages from loggining service separated by ',' and from message service separated by '\n'>"}
        or 
        {"status": "<status code>"} if errors occured
    """
    async with httpx.AsyncClient() as client:
        all_messages_response = await client.get(url=LOGGINING_SERVICE_DOCKER+"/get_fetched_messages")
        static_text_response = await client.get(url=MESSAGES_SERVICE_DOCKER+"/message_handler")

        if all_messages_response.status_code != 200:
            return {"status": all_messages_response.status_code}
        elif static_text_response.status_code != 200:
            return {"status": static_text_response.status_code}
        
    all_messages_json = all_messages_response.json()
    static_text_json = static_text_response.json()

    response = all_messages_json["msgs"] + "\n" + static_text_json["static_text"]
    return {"all_msgs": response}
