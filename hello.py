from dotenv import load_dotenv
import os
import pdb

load_dotenv()

print(os.getenv("DATA_DIR"))


from langgraph_sdk import get_sync_client

client = get_sync_client(url="http://localhost:8123")

# print(dir(client))
# pdb.set_trace()

# assistants = client.assistants.search()
# print(f"assistants: {assistants}")

# print(dir(client))

assistant = client.assistants.search(graph_id="agent")[0]
print(assistant)
# assistant = client.assistants.create(graph_id="agent")
# thread = client.threads.get()

input_message = "What are the products of CCS?"

runs = client.runs.stream(
    None,
    assistant_id=assistant["assistant_id"],
    input={"messages": [{"role": "user", "content": input_message}]},
    stream_mode="values",
)


final_response = [chunk for chunk in runs][-1]
data = final_response.data["messages"][-1]
print(data["content"])
