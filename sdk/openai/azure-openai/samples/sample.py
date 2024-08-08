# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

import os

import dotenv
from azure.identity import get_bearer_token_provider, DefaultAzureCredential
from azure.openai import AzureOpenAI
from azure.openai.types.chat.on_your_data import AzureCognitiveSearchChatExtensionConfiguration, AzureCognitiveSearchChatExtensionParameters

dotenv.load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_ad_token_provider=get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"),
    api_version="2024-07-01-preview",
)

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Does Azure OpenAI support customer managed keys?",
        },
        {
            "role": "assistant",
            "content": "Yes, customer managed keys are supported by Azure OpenAI.",
        },
        {"role": "user", "content": "Do other Azure AI services support this too?"},
    ],
    data_sources=[
            AzureCognitiveSearchChatExtensionConfiguration(
                type="azure_search",
                parameters=AzureCognitiveSearchChatExtensionParameters(
                    authentication={"type": "system_assigned_managed_identity"},
                    endpoint=os.environ["AZURE_OPENAI_SEARCH_ENDPOINT"],
                    index_name=os.environ["AZURE_OPENAI_SEARCH_INDEX"],
                )
            )
        ]
)
print(response)

# response = client.chat.completions.create(
#     model="gpt-4",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {
#             "role": "user",
#             "content": "Does Azure OpenAI support customer managed keys?",
#         },
#         {
#             "role": "assistant",
#             "content": "Yes, customer managed keys are supported by Azure OpenAI.",
#         },
#         {"role": "user", "content": "Do other Azure AI services support this too?"},
#     ],
#     stream=True
# )

# for chunk in response:
#     print(chunk)



# assistant = client.beta.assistants.create(model="gpt-4", tools=[{"type": "browser", "browser": {}}])