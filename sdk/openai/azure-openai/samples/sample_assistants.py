import os

import dotenv
from openai import AssistantEventHandler

from azure.openai import AzureOpenAI, parse_azure, parse_azure_wrapper
from azure.openai.types.beta.assistants import CustomToolParam, AzureToolCall, AzureText, AzureAssistant

dotenv.load_dotenv()


class EventHandler(AssistantEventHandler):
    def __init__(self, client, thread_id, assistant_id):
        super().__init__()
        self.client = client
        self.thread_id = thread_id
        self.assistant_id = assistant_id

    @parse_azure_wrapper
    def on_tool_call_created(self, tool_call: AzureToolCall):
        if tool_call.type == "custom":
            print("started calling the custom tool")

    @parse_azure_wrapper
    def on_tool_call_done(self, tool_call: AzureToolCall) -> None:
        if tool_call.type == "custom":
            print("completed calling the custom tool")

    @parse_azure_wrapper
    def on_text_done(self, text: AzureText) -> None:
        result = text.value
        for annotation in text.annotations:
            if annotation.type == "url_citation":
                result = text.value.replace(
                    annotation.text, "[{}]({})".format(annotation.url_citation.title, annotation.url_citation.url)
                )
                print(result)


client = AzureOpenAI()


assistant = client.beta.assistants.create(
    name="Travel planner copilot",
    instructions="You are travel planner that helps people plan travels across the world",
    tools=[
        CustomToolParam(
            type="custom",
            custom={"custom": ""}
        ),
    ],
    model="gpt-4",
)

azure: AzureAssistant = parse_azure(assistant)
thread = client.beta.threads.create()

while True:
    user_input = input("Your input: ")
    message = client.beta.threads.messages.create(thread_id=thread.id, role="user", content=user_input)
    event_handler = EventHandler(client, thread.id, assistant.id)
    with client.beta.threads.runs.stream(
        assistant_id=assistant.id, thread_id=thread.id, event_handler=event_handler
    ) as stream:
        stream.until_done()
