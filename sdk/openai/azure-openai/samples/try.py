import os
import threading
import dotenv
from azure.openai import OpenAIClient
from azure.core.credentials import AzureKeyCredential

dotenv.load_dotenv()


client = OpenAIClient(endpoint="https://sdk8428.openai.azure.com/", credential=AzureKeyCredential(os.environ["OPENAI_API_KEY"]))

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "How do I bake a chocolate cake?"}
]

def hello(p, d, _):
    return d

response = client.get_chat_completions(deployment_id="gpt-4", body={"messages": messages, "stream": True}, stream=True, cls=hello)

for r in response:
    if len(r.choices) > 0:
        print(r.choices[0].delta.content, end="", flush=True)
