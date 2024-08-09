# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

import os
import dotenv
from azure.openai import AzureOpenAI, parse_azure
from azure.openai.types.chat import (
    AzureChatExtras,
    AzureCognitiveSearchChatExtensionConfiguration,
    AzureCognitiveSearchChatExtensionParameters,
)

dotenv.load_dotenv()

client = AzureOpenAI()

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
    extra_body=AzureChatExtras(
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
)

azure_response = parse_azure(response)
print(azure_response.prompt_filter_results)
