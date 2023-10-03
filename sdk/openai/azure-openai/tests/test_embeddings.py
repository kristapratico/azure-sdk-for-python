# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

import pytest
import openai
from devtools_testutils import AzureRecordedTestCase
from conftest import configure, AZURE, OPENAI, ALL


class TestEmbeddings(AzureRecordedTestCase):

    @pytest.mark.skip()
    @pytest.mark.parametrize("api_type", [AZURE])
    def test_embedding_bad_deployment_name(self, client, azure_openai_creds, api_type):
        with pytest.raises(openai.error.InvalidRequestError) as e:
            client.embeddings.create(input="hello world", deployment_id="deployment")
        assert e.value.http_status == 404
        assert "The API deployment for this resource does not exist" in str(e.value)

    @pytest.mark.skip()
    @pytest.mark.parametrize("api_type", [AZURE])
    def test_embedding_kw_input(self, client, azure_openai_creds, api_type):
        deployment = azure_openai_creds["embeddings_name"]

        embedding = client.embeddings.create(input="hello world", deployment_id=deployment)
        assert embedding
        embedding = client.embeddings.create(input="hello world", engine=deployment)
        assert embedding
        with pytest.raises(openai.error.InvalidRequestError) as e:
            client.embeddings.create(input="hello world", model=deployment)
        assert "Must provide an 'engine' or 'deployment_id' parameter" in str(e.value)

    @pytest.mark.parametrize("api_type", ALL)
    def test_embedding(self, client, azure_openai_creds, api_type):
        model = azure_openai_creds["embeddings_model"] if api_type == "openai" \
          else azure_openai_creds["embeddings_name"]

        embedding = client.embeddings.create(input="hello world", model=model)
        assert embedding.object == "list"
        assert embedding.model
        assert embedding.usage.prompt_tokens is not None
        assert embedding.usage.total_tokens is not None
        assert len(embedding.data) == 1
        assert embedding.data[0].object == "embedding"
        assert embedding.data[0].index is not None
        assert len(embedding.data[0].embedding) > 0

    @pytest.mark.parametrize("api_type", [AZURE, OPENAI])
    def test_embedding_batched(self, client, azure_openai_creds, api_type):
        model = azure_openai_creds["embeddings_model"] if api_type == "openai" \
          else azure_openai_creds["embeddings_name"]
        embedding = client.embeddings.create(input=["hello world", "second input"], model=model)
        assert embedding.object == "list"
        assert embedding.model
        assert embedding.usage.prompt_tokens is not None
        assert embedding.usage.total_tokens is not None
        assert len(embedding.data) == 2
        assert embedding.data[0].object == "embedding"
        assert embedding.data[0].index is not None
        assert len(embedding.data[0].embedding) > 0

    @pytest.mark.parametrize("api_type", [AZURE, OPENAI])
    def test_embedding_user(self, client, azure_openai_creds, api_type):
        model = azure_openai_creds["embeddings_model"] if api_type == "openai" \
          else azure_openai_creds["embeddings_name"]

        embedding = client.embeddings.create(input="hello world", user="krista", model=model)
        assert embedding.object == "list"
        assert embedding.model
        assert embedding.usage.prompt_tokens is not None
        assert embedding.usage.total_tokens is not None
        assert len(embedding.data) == 1
        assert embedding.data[0].object == "embedding"
        assert embedding.data[0].index is not None
        assert len(embedding.data[0].embedding) > 0
