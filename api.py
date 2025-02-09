from langgraph_sdk import get_sync_client
from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
import os

load_dotenv()

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


URL = os.getenv("CHAT_API_URL")
print("=========URL========")
print(URL)

app = FastAPI()

client = get_sync_client(url="http://localhost:8123")

assistant = client.assistants.search(graph_id="agent")[0]


@app.get("/hello")
def hello():
    return {"hello": "world"}


@app.post("/chat")
async def chat(request: ChatRequest):
    user_message = request.message

    runs = client.runs.stream(
        None,
        assistant_id=assistant["assistant_id"],
        input={"messages": [{"role": "user", "content": user_message}]},
        stream_mode="values",
    )

    final_response = [chunk for chunk in runs][-1]
    data = final_response.data["messages"][-1]

    return {"message": data["content"]}


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)
