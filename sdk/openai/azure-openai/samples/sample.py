import openai
from azure.openai import login
from azure.identity import DefaultAzureCredential


credential = DefaultAzureCredential()
with login(endpoint="", credential=credential):
    completion = openai.Completion.create(prompt="hello", engine="gpt4")
    print(completion)
