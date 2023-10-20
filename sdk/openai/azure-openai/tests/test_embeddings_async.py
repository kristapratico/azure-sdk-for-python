# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

import pytest
import openai
from devtools_testutils import AzureRecordedTestCase
from conftest import configure_async, AZURE, OPENAI, ALL


class TestEmbeddingsAsync(AzureRecordedTestCase):

    @pytest.mark.skip()
    @configure_async
    @pytest.mark.asyncio
    @pytest.mark.parametrize("api_type", [AZURE])
    async def test_embedding_bad_deployment_name(self, client_async, azure_openai_creds, api_type, **kwargs):
        with pytest.raises(openai.error.InvalidRequestError) as e:
            await client_async.embeddings.create(input="hello world", deployment_id="deployment")
        assert e.value.http_status == 404
        assert "The API deployment for this resource does not exist" in str(e.value)

    @pytest.mark.skip()
    @configure_async
    @pytest.mark.asyncio
    @pytest.mark.parametrize("api_type", [AZURE])
    async def test_embedding_kw_input(self, client_async, azure_openai_creds, api_type, **kwargs):
        deployment = client_async, azure_openai_creds["embeddings_name"]

        embedding = await client_async.embeddings.create(input="hello world", deployment_id=deployment)
        assert embedding
        embedding = await client_async.embeddings.create(input="hello world", engine=deployment)
        assert embedding
        with pytest.raises(openai.error.InvalidRequestError) as e:
            await client_async.embeddings.create(input="hello world", model=deployment)
        assert "Must provide an 'engine' or 'deployment_id' parameter" in str(e.value)

    @configure_async
    @pytest.mark.asyncio
    @pytest.mark.parametrize("api_type", ALL)
    async def test_embedding(self, client_async, azure_openai_creds, api_type, **kwargs):

        embedding = await client_async.embeddings.create(input="hello world", **kwargs)
        assert embedding.usage.prompt_tokens is not None
        assert embedding.usage.total_tokens is not None
        assert len(embedding.data) == 1
        assert embedding.data[0].index is not None
        assert len(embedding.data[0].embedding) > 0

    @configure_async
    @pytest.mark.asyncio
    @pytest.mark.parametrize("api_type", [AZURE, OPENAI])
    async def test_embedding_batched(self, client_async, azure_openai_creds, api_type, **kwargs):

        embedding = await client_async.embeddings.create(input=["hello world", "second input"], **kwargs)
        assert embedding.usage.prompt_tokens is not None
        assert embedding.usage.total_tokens is not None
        assert len(embedding.data) == 2
        assert embedding.data[0].index is not None
        assert len(embedding.data[0].embedding) > 0

    @configure_async
    @pytest.mark.asyncio
    @pytest.mark.parametrize("api_type", [AZURE, OPENAI])
    async def test_embedding_user(self, client_async, azure_openai_creds, api_type, **kwargs):

        embedding = await client_async.embeddings.create(input="hello world", user="krista", **kwargs)
        assert embedding.usage.prompt_tokens is not None
        assert embedding.usage.total_tokens is not None
        assert len(embedding.data) == 1
        assert embedding.data[0].index is not None
        assert len(embedding.data[0].embedding) > 0
