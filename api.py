from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langgraph_sdk import get_sync_client
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn
import os

load_dotenv()


class ChatRequest(BaseModel):
    message: str


origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "https://dev.ccsfusion.com",
    "https://app.linkfusions.com",
    "https://aiagent.linkfusions.com",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = get_sync_client(url="http://localhost:8123")

assistant = client.assistants.search(graph_id="agent")[0]


@app.options("/{full_path:path}")
async def preflight_check():
    return {"message": "CORS preflight OK"}


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
