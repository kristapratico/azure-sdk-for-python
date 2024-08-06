# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

from openai import AzureOpenAI as SyncClient, Stream
from openai.resources.chat import Chat as OpenAIChat, Completions as OpenAICompletions
from azure.openai.types.chat.content_filtering import AzureChatCompletionChunk


class Completions(OpenAICompletions):
    def __getattribute__(self, name):
        if name == "create":

            def create_wrapper(*args, **kwargs):
                # modify request body for any azure-only options
                if "data_sources" in kwargs:
                    kwargs["extra_body"] = kwargs.pop("data_sources")

                result = super(Completions, self).__getattribute__("create")(*args, **kwargs)
                # transform response for any azure-only options?
                if "stream" in kwargs and kwargs["stream"] is True:
                    return Stream(cast_to=AzureChatCompletionChunk, response=result.response, client=result._client)
                return result
            return create_wrapper
        return super().__getattribute__(name)


class Chat(OpenAIChat):
    def __getattribute__(self, name):
        if name == "completions":
            return Completions(self._client)
        return super().__getattribute__(name)


class AzureOpenAI(SyncClient):
    def __getattribute__(self, name):
        if name == "chat":
            return Chat(self)
        return super().__getattribute__(name)
