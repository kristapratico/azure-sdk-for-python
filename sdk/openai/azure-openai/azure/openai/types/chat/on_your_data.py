# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

from __future__ import annotations

from typing import List, Optional, Union
from typing_extensions import Literal, Required, TypedDict

# TODO these models come from an older API version

__all__ = [
    "AzureChatEnhancementConfiguration",
    "AzureChatGroundingEnhancementConfiguration",
    "AzureChatOCREnhancementConfiguration",
    "AzureCognitiveSearchChatExtensionConfiguration",
    "AzureCognitiveSearchChatExtensionParameters",
    "AzureCognitiveSearchIndexFieldMappingOptions",
    "AzureCosmosDBChatExtensionConfiguration",
    "AzureCosmosDBChatExtensionParameters",
    "AzureCosmosDBFieldMappingOptions",
    "AzureMachineLearningIndexChatExtensionConfiguration",
    "AzureMachineLearningIndexChatExtensionParameters",
    "ElasticsearchChatExtensionConfiguration",
    "ElasticsearchChatExtensionParameters",
    "ElasticsearchIndexFieldMappingOptions",
    "OnYourDataAccessTokenAuthenticationOptions",
    "OnYourDataApiKeyAuthenticationOptions",
    "OnYourDataConnectionStringAuthenticationOptions",
    "OnYourDataDeploymentNameVectorizationSource",
    "OnYourDataEncodedApiKeyAuthenticationOptions",
    "OnYourDataEndpointVectorizationSource",
    "OnYourDataKeyAndKeyIdAuthenticationOptions",
    "OnYourDataModelIdVectorizationSource",
    "OnYourDataSystemAssignedManagedIdentityAuthenticationOptions",
    "OnYourDataUserAssignedManagedIdentityAuthenticationOptions",
    "PineconeChatExtensionConfiguration",
    "PineconeChatExtensionParameters",
    "PineconeFieldMappingOptions",
    "AzureChatExtensionType",
    "OnYourDataAuthenticationType",
    "OnYourDataVectorizationSourceType",
    "AzureCognitiveSearchQueryType",
    "ElasticsearchQueryType",
    "AzureChatExtensionConfiguration",
]

AzureChatExtensionType = Literal["AzureCognitiveSearch", "AzureMLIndex", "AzureCosmosDB", "Elasticsearch", "Pinecone"]
OnYourDataAuthenticationType = Literal[
    "APIKey",
    "ConnectionString",
    "KeyAndKeyId",
    "EncodedAPIKey",
    "AccessToken",
    "SystemAssignedManagedIdentity",
    "UserAssignedManagedIdentity",
]
OnYourDataVectorizationSourceType = Literal["Endpoint", "DeploymentName", "ModelId"]
AzureCognitiveSearchQueryType = Literal["simple", "semantic", "vector", "vectorSimpleHybrid", "vectorSemanticHybrid"]
ElasticsearchQueryType = Literal["simple", "vector"]

AzureChatExtensionConfiguration = Union[
    "AzureCognitiveSearchChatExtensionConfiguration",
    "AzureCosmosDBChatExtensionConfiguration",
    "AzureMachineLearningIndexChatExtensionConfiguration",
    "ElasticsearchChatExtensionConfiguration",
    "PineconeChatExtensionConfiguration",
]


class AzureChatEnhancementConfiguration(TypedDict, total=False):

    grounding: Optional[AzureChatGroundingEnhancementConfiguration]
    """A representation of the available options for the Azure OpenAI grounding enhancement."""
    ocr: Optional[AzureChatOCREnhancementConfiguration]
    """A representation of the available options for the Azure OpenAI optical character recognition
     (OCR) enhancement."""


class AzureChatGroundingEnhancementConfiguration(TypedDict, total=False):

    enabled: Required[bool]
    """Specifies whether the enhancement is enabled. Required."""


class AzureChatOCREnhancementConfiguration(TypedDict, total=False):

    enabled: Required[bool]
    """Specifies whether the enhancement is enabled. Required."""


class AzureCognitiveSearchChatExtensionConfiguration(TypedDict, total=False):

    type: Required[Literal["AzureCognitiveSearch"]]
    """The type label to use when configuring Azure OpenAI chat extensions. This should typically not
     be changed from its
     default value for Azure Cognitive Search. Required. Represents the use of Azure Cognitive
     Search as an Azure OpenAI chat extension."""
    parameters: Required[AzureCognitiveSearchChatExtensionParameters]
    """The parameters to use when configuring Azure Cognitive Search. Required."""


class AzureCognitiveSearchChatExtensionParameters(TypedDict, total=False):

    authentication: Optional[
        Union[
            OnYourDataApiKeyAuthenticationOptions,
            OnYourDataAccessTokenAuthenticationOptions,
            OnYourDataConnectionStringAuthenticationOptions,
            OnYourDataEncodedApiKeyAuthenticationOptions,
            OnYourDataKeyAndKeyIdAuthenticationOptions,
            OnYourDataSystemAssignedManagedIdentityAuthenticationOptions,
            OnYourDataUserAssignedManagedIdentityAuthenticationOptions,
        ]
    ]
    """The authentication method to use when accessing the defined data source.
     Each data source type supports a specific set of available authentication methods; please see
     the documentation of
     the data source for supported mechanisms.
     If not otherwise provided, On Your Data will attempt to use System Managed Identity (default
     credential)
     authentication."""
    top_n_documents: Optional[int]
    """The configured top number of documents to feature for the configured query."""
    in_scope: Optional[bool]
    """Whether queries should be restricted to use of indexed data."""
    strictness: Optional[int]
    """The configured strictness of the search relevance filtering. The higher of strictness, the
     higher of the precision but lower recall of the answer."""
    role_information: Optional[str]
    """Give the model instructions about how it should behave and any context it should reference when
     generating a response. You can describe the assistant's personality and tell it how to format
     responses. There's a 100 token limit for it, and it counts against the overall token limit."""
    endpoint: Required[str]
    """The absolute endpoint path for the Azure Cognitive Search resource to use. Required."""
    index_name: Required[str]
    """The name of the index to use as available in the referenced Azure Cognitive Search resource.
     Required."""
    key: Optional[str]
    """The API key to use when interacting with the Azure Cognitive Search resource."""
    fields_mapping: Optional[AzureCognitiveSearchIndexFieldMappingOptions]
    """Customized field mapping behavior to use when interacting with the search index."""
    query_type: Optional[AzureCognitiveSearchQueryType]
    """The query type to use with Azure Cognitive Search. Known values are: \"simple\", \"semantic\",
     \"vector\", \"vectorSimpleHybrid\", and \"vectorSemanticHybrid\"."""
    semantic_configuration: Optional[str]
    """The additional semantic configuration for the query."""
    filter: Optional[str]
    """Search filter."""
    embedding_endpoint: Optional[str]
    """When using embeddings for search, specifies the resource endpoint URL from which embeddings
     should be retrieved. It should be in the format of format
     https://YOUR_RESOURCE_NAME.openai.azure.com/openai/deployments/YOUR_DEPLOYMENT_NAME/embeddings?api-version={api-version}."""
    embedding_key: Optional[str]
    """When using embeddings, specifies the API key to use with the provided embeddings endpoint."""
    embedding_dependency: Optional[
        Union[
            OnYourDataDeploymentNameVectorizationSource,
            OnYourDataEndpointVectorizationSource,
            OnYourDataModelIdVectorizationSource,
        ]
    ]
    """The embedding dependency for vector search."""


class AzureCognitiveSearchIndexFieldMappingOptions(TypedDict, total=False):

    title_field: Optional[str]
    """The name of the index field to use as a title."""
    url_field: Optional[str]
    """The name of the index field to use as a URL."""
    filepath_field: Optional[str]
    """The name of the index field to use as a filepath."""
    content_fields: Optional[List[str]]
    """The names of index fields that should be treated as content."""
    content_fields_separator: Optional[str]
    """The separator pattern that content fields should use."""
    vector_fields: Optional[List[str]]
    """The names of fields that represent vector data."""
    imagevector_fields: Optional[List[str]]
    """The names of fields that represent image vector data."""


class AzureCosmosDBChatExtensionConfiguration(TypedDict, total=False):

    type: Required[Literal["AzureCosmosDB"]]
    """The type label to use when configuring Azure OpenAI chat extensions. This should typically not
     be changed from its
     default value for Azure Cosmos DB. Required. Represents the use of Azure Cosmos DB as an Azure
     OpenAI chat extension."""
    parameters: Required[AzureCosmosDBChatExtensionParameters]
    """The parameters to use when configuring Azure OpenAI CosmosDB chat extensions. Required."""


class AzureCosmosDBChatExtensionParameters(TypedDict, total=False):

    authentication: Optional[
        Union[
            OnYourDataApiKeyAuthenticationOptions,
            OnYourDataAccessTokenAuthenticationOptions,
            OnYourDataConnectionStringAuthenticationOptions,
            OnYourDataEncodedApiKeyAuthenticationOptions,
            OnYourDataKeyAndKeyIdAuthenticationOptions,
            OnYourDataSystemAssignedManagedIdentityAuthenticationOptions,
            OnYourDataUserAssignedManagedIdentityAuthenticationOptions,
        ]
    ]
    """The authentication method to use when accessing the defined data source.
     Each data source type supports a specific set of available authentication methods; please see
     the documentation of
     the data source for supported mechanisms.
     If not otherwise provided, On Your Data will attempt to use System Managed Identity (default
     credential)
     authentication."""
    top_n_documents: Optional[int]
    """The configured top number of documents to feature for the configured query."""
    in_scope: Optional[bool]
    """Whether queries should be restricted to use of indexed data."""
    strictness: Optional[int]
    """The configured strictness of the search relevance filtering. The higher of strictness, the
     higher of the precision but lower recall of the answer."""
    role_information: Optional[str]
    """Give the model instructions about how it should behave and any context it should reference when
     generating a response. You can describe the assistant's personality and tell it how to format
     responses. There's a 100 token limit for it, and it counts against the overall token limit."""
    database_name: Required[str]
    """The MongoDB vCore database name to use with Azure Cosmos DB. Required."""
    container_name: Required[str]
    """The name of the Azure Cosmos DB resource container. Required."""
    index_name: Required[str]
    """The MongoDB vCore index name to use with Azure Cosmos DB. Required."""
    fields_mapping: Required[AzureCosmosDBFieldMappingOptions]
    """Customized field mapping behavior to use when interacting with the search index. Required."""
    embedding_dependency: Required[
        Union[
            OnYourDataDeploymentNameVectorizationSource,
            OnYourDataEndpointVectorizationSource,
            OnYourDataModelIdVectorizationSource,
        ]
    ]
    """The embedding dependency for vector search. Required."""


class AzureCosmosDBFieldMappingOptions(TypedDict, total=False):

    title_field: Optional[str]
    """The name of the index field to use as a title."""
    url_field: Optional[str]
    """The name of the index field to use as a URL."""
    filepath_field: Optional[str]
    """The name of the index field to use as a filepath."""
    content_fields: Required[List[str]]
    """The names of index fields that should be treated as content. Required."""
    content_fields_separator: Optional[str]
    """The separator pattern that content fields should use."""
    vector_fields: Required[List[str]]
    """The names of fields that represent vector data. Required."""


class AzureMachineLearningIndexChatExtensionConfiguration(TypedDict, total=False):

    type: Required[Literal["AzureMLIndex"]]
    """The type label to use when configuring Azure OpenAI chat extensions. This should typically not
     be changed from its
     default value for Azure Machine Learning vector index. Required. Represents the use of Azure
     Machine Learning index as an Azure OpenAI chat extension."""
    parameters: Required[AzureMachineLearningIndexChatExtensionParameters]
    """The parameters for the Azure Machine Learning vector index chat extension. Required."""


class AzureMachineLearningIndexChatExtensionParameters(TypedDict, total=False):

    authentication: Optional[
        Union[
            OnYourDataApiKeyAuthenticationOptions,
            OnYourDataAccessTokenAuthenticationOptions,
            OnYourDataConnectionStringAuthenticationOptions,
            OnYourDataEncodedApiKeyAuthenticationOptions,
            OnYourDataKeyAndKeyIdAuthenticationOptions,
            OnYourDataSystemAssignedManagedIdentityAuthenticationOptions,
            OnYourDataUserAssignedManagedIdentityAuthenticationOptions,
        ]
    ]
    """The authentication method to use when accessing the defined data source.
     Each data source type supports a specific set of available authentication methods; please see
     the documentation of
     the data source for supported mechanisms.
     If not otherwise provided, On Your Data will attempt to use System Managed Identity (default
     credential)
     authentication."""
    top_n_documents: Optional[int]
    """The configured top number of documents to feature for the configured query."""
    in_scope: Optional[bool]
    """Whether queries should be restricted to use of indexed data."""
    strictness: Optional[int]
    """The configured strictness of the search relevance filtering. The higher of strictness, the
     higher of the precision but lower recall of the answer."""
    role_information: Optional[str]
    """Give the model instructions about how it should behave and any context it should reference when
     generating a response. You can describe the assistant's personality and tell it how to format
     responses. There's a 100 token limit for it, and it counts against the overall token limit."""
    project_resource_id: Required[str]
    """The resource ID of the Azure Machine Learning project. Required."""
    name: Required[str]
    """The Azure Machine Learning vector index name. Required."""
    version: Required[str]
    """The version of the Azure Machine Learning vector index. Required."""
    filter: Optional[str]
    """Search filter. Only supported if the Azure Machine Learning vector index is of type
     AzureSearch."""


class ElasticsearchChatExtensionConfiguration(TypedDict, total=False):

    type: Required[Literal["Elasticsearch"]]
    """The type label to use when configuring Azure OpenAI chat extensions. This should typically not
     be changed from its
     default value for Elasticsearch®. Required. Represents the use of Elasticsearch® index as an
     Azure OpenAI chat extension."""
    parameters: Required[ElasticsearchChatExtensionParameters]
    """The parameters to use when configuring Elasticsearch®. Required."""


class ElasticsearchChatExtensionParameters(TypedDict, total=False):

    authentication: Optional[
        Union[
            OnYourDataApiKeyAuthenticationOptions,
            OnYourDataAccessTokenAuthenticationOptions,
            OnYourDataConnectionStringAuthenticationOptions,
            OnYourDataEncodedApiKeyAuthenticationOptions,
            OnYourDataKeyAndKeyIdAuthenticationOptions,
            OnYourDataSystemAssignedManagedIdentityAuthenticationOptions,
            OnYourDataUserAssignedManagedIdentityAuthenticationOptions,
        ]
    ]
    """The authentication method to use when accessing the defined data source.
     Each data source type supports a specific set of available authentication methods; please see
     the documentation of
     the data source for supported mechanisms.
     If not otherwise provided, On Your Data will attempt to use System Managed Identity (default
     credential)
     authentication."""
    top_n_documents: Optional[int]
    """The configured top number of documents to feature for the configured query."""
    in_scope: Optional[bool]
    """Whether queries should be restricted to use of indexed data."""
    strictness: Optional[int]
    """The configured strictness of the search relevance filtering. The higher of strictness, the
     higher of the precision but lower recall of the answer."""
    role_information: Optional[str]
    """Give the model instructions about how it should behave and any context it should reference when
     generating a response. You can describe the assistant's personality and tell it how to format
     responses. There's a 100 token limit for it, and it counts against the overall token limit."""
    endpoint: Required[str]
    """The endpoint of Elasticsearch®. Required."""
    index_name: Required[str]
    """The index name of Elasticsearch®. Required."""
    fields_mapping: Optional[ElasticsearchIndexFieldMappingOptions]
    """The index field mapping options of Elasticsearch®."""
    query_type: Optional[ElasticsearchQueryType]
    """The query type of Elasticsearch®. Known values are: \"simple\" and \"vector\"."""
    embedding_dependency: Optional[
        Union[
            OnYourDataDeploymentNameVectorizationSource,
            OnYourDataEndpointVectorizationSource,
            OnYourDataModelIdVectorizationSource,
        ]
    ]
    """The embedding dependency for vector search."""


class ElasticsearchIndexFieldMappingOptions(TypedDict, total=False):

    title_field: Optional[str]
    """The name of the index field to use as a title."""
    url_field: Optional[str]
    """The name of the index field to use as a URL."""
    filepath_field: Optional[str]
    """The name of the index field to use as a filepath."""
    content_fields: Optional[List[str]]
    """The names of index fields that should be treated as content."""
    content_fields_separator: Optional[str]
    """The separator pattern that content fields should use."""
    vector_fields: Optional[List[str]]
    """The names of fields that represent vector data."""


class OnYourDataAccessTokenAuthenticationOptions(TypedDict, total=False):

    type: Required[Literal["AccessToken"]]
    """The authentication type of access token. Required. Authentication via access token."""
    access_token: Required[str]
    """The access token to use for authentication. Required."""


class OnYourDataApiKeyAuthenticationOptions(TypedDict, total=False):

    type: Required[Literal["APIKey"]]
    """The authentication type of API key. Required. Authentication via API key."""
    key: Required[str]
    """The API key to use for authentication. Required."""


class OnYourDataConnectionStringAuthenticationOptions(TypedDict, total=False):

    type: Required[Literal["ConnectionString"]]
    """The authentication type of connection string. Required. Authentication via connection string."""
    connection_string: Required[str]
    """The connection string to use for authentication. Required."""


class OnYourDataDeploymentNameVectorizationSource(TypedDict, total=False):

    type: Required[Literal["DeploymentName"]]
    """The type of vectorization source to use. Always 'DeploymentName' for this type. Required.
     Represents an Ada model deployment name to use. This model deployment must be in the same Azure
     OpenAI resource, but
     On Your Data will use this model deployment via an internal call rather than a public one,
     which enables vector
     search even in private networks."""
    deployment_name: Required[str]
    """The embedding model deployment name within the same Azure OpenAI resource. This enables you to
     use vector search without Azure OpenAI api-key and without Azure OpenAI public network access.
     Required."""


class OnYourDataEncodedApiKeyAuthenticationOptions(TypedDict, total=False):

    type: Required[Literal["EncodedAPIKey"]]
    """The authentication type of Elasticsearch encoded API Key. Required. Authentication via encoded
     API key."""
    encoded_api_key: Required[str]
    """The encoded API key to use for authentication. Required."""


class OnYourDataEndpointVectorizationSource(TypedDict, total=False):

    type: Required[Literal["Endpoint"]]
    """The type of vectorization source to use. Always 'Endpoint' for this type. Required. Represents
     vectorization performed by public service calls to an Azure OpenAI embedding model."""
    endpoint: Required[str]
    """Specifies the resource endpoint URL from which embeddings should be retrieved. It should be in
     the format of
     https://YOUR_RESOURCE_NAME.openai.azure.com/openai/deployments/YOUR_DEPLOYMENT_NAME/embeddings.
     The api-version query parameter is not allowed. Required."""
    authentication: Required[
        Optional[
            Union[
                OnYourDataApiKeyAuthenticationOptions,
                OnYourDataAccessTokenAuthenticationOptions,
                OnYourDataConnectionStringAuthenticationOptions,
                OnYourDataEncodedApiKeyAuthenticationOptions,
                OnYourDataKeyAndKeyIdAuthenticationOptions,
                OnYourDataSystemAssignedManagedIdentityAuthenticationOptions,
                OnYourDataUserAssignedManagedIdentityAuthenticationOptions,
            ]
        ]
    ]
    """Specifies the authentication options to use when retrieving embeddings from the specified
     endpoint. Required."""


class OnYourDataKeyAndKeyIdAuthenticationOptions(TypedDict, total=False):

    type: Required[Literal["KeyAndKeyId"]]
    """The authentication type of Elasticsearch key and key ID pair. Required. Authentication via key
     and key ID pair."""
    key: Required[str]
    """The key to use for authentication. Required."""
    key_id: Required[str]
    """The key ID to use for authentication. Required."""


class OnYourDataModelIdVectorizationSource(TypedDict, total=False):

    type: Required[Literal["ModelId"]]
    """The type of vectorization source to use. Always 'ModelId' for this type. Required. Represents a
     specific embedding model ID as defined in the search service.
     Currently only supported by Elasticsearch®."""
    model_id: Required[str]
    """The embedding model ID build inside the search service. Currently only supported by
     Elasticsearch®. Required."""


class OnYourDataSystemAssignedManagedIdentityAuthenticationOptions(TypedDict, total=False):

    type: Required[Literal["SystemAssignedManagedIdentity"]]
    """The authentication type of system-assigned managed identity. Required. Authentication via
     system-assigned managed identity."""


class OnYourDataUserAssignedManagedIdentityAuthenticationOptions(TypedDict, total=False):
    type: Required[Literal["UserAssignedManagedIdentity"]]
    """The authentication type of user-assigned managed identity. Required. Authentication via
     user-assigned managed identity."""
    managed_identity_resource_id: Required[str]
    """The resource ID of the user-assigned managed identity to use for authentication. Required."""


class PineconeChatExtensionConfiguration(TypedDict, total=False):

    type: Required[Literal["Pinecone"]]
    """The type label to use when configuring Azure OpenAI chat extensions. This should typically not
     be changed from its
     default value for Pinecone. Required. Represents the use of Pinecone index as an Azure OpenAI
     chat extension."""
    parameters: Required[PineconeChatExtensionParameters]
    """The parameters to use when configuring Azure OpenAI chat extensions. Required."""


class PineconeChatExtensionParameters(TypedDict, total=False):

    authentication: Optional[
        Union[
            OnYourDataApiKeyAuthenticationOptions,
            OnYourDataAccessTokenAuthenticationOptions,
            OnYourDataConnectionStringAuthenticationOptions,
            OnYourDataEncodedApiKeyAuthenticationOptions,
            OnYourDataKeyAndKeyIdAuthenticationOptions,
            OnYourDataSystemAssignedManagedIdentityAuthenticationOptions,
            OnYourDataUserAssignedManagedIdentityAuthenticationOptions,
        ]
    ]
    """The authentication method to use when accessing the defined data source.
     Each data source type supports a specific set of available authentication methods; please see
     the documentation of
     the data source for supported mechanisms.
     If not otherwise provided, On Your Data will attempt to use System Managed Identity (default
     credential)
     authentication."""
    top_n_documents: Optional[int]
    """The configured top number of documents to feature for the configured query."""
    in_scope: Optional[bool]
    """Whether queries should be restricted to use of indexed data."""
    strictness: Optional[int]
    """The configured strictness of the search relevance filtering. The higher of strictness, the
     higher of the precision but lower recall of the answer."""
    role_information: Optional[str]
    """Give the model instructions about how it should behave and any context it should reference when
     generating a response. You can describe the assistant's personality and tell it how to format
     responses. There's a 100 token limit for it, and it counts against the overall token limit."""
    environment: Required[str]
    """The environment name of Pinecone. Required."""
    index_name: Required[str]
    """The name of the Pinecone database index. Required."""
    fields_mapping: Required[PineconeFieldMappingOptions]
    """Customized field mapping behavior to use when interacting with the search index. Required."""
    embedding_dependency: Required[
        Union[
            OnYourDataDeploymentNameVectorizationSource,
            OnYourDataEndpointVectorizationSource,
            OnYourDataModelIdVectorizationSource,
        ]
    ]
    """The embedding dependency for vector search. Required."""


class PineconeFieldMappingOptions(TypedDict, total=False):

    title_field: Optional[str]
    """The name of the index field to use as a title."""
    url_field: Optional[str]
    """The name of the index field to use as a URL."""
    filepath_field: Optional[str]
    """The name of the index field to use as a filepath."""
    content_fields: Required[List[str]]
    """The names of index fields that should be treated as content. Required."""
    content_fields_separator: Optional[str]
    """The separator pattern that content fields should use."""
