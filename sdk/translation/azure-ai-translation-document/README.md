# Azure Document Translation client library for Python

Azure Cognitive Services Document Translation is a cloud service that translates documents to and from 90 languages 
and dialects while preserving document structure and data format. Use the client library for Document Translation to:

* Translate numerous, large files from an Azure Blob Storage container to a target container in your language of choice.
* Check the translation status and progress of each document in the translation job.
* Apply a custom translation model or glossaries to tailor translation to your specific case.

[Source code][python-dt-src] | [Package (PyPI)][python-dt-pypi] | [API reference documentation][python-dt-ref-docs] | [Product documentation][python-dt-product-docs] | [Samples][python-dt-samples]

## Getting started

### Prerequisites
* Python 2.7, or 3.6 or later is required to use this package.
* You must have an [Azure subscription][azure_subscription] and a
[Document Translation resource][DT_resource] to use this package.

### Install the package
Install the Azure Document Translation client library for Python with [pip][pip]:

```bash
pip install azure-ai-translation-document --pre
```

> Note: This version of the client library defaults to the v1.0-preview.1 version of the service

#### Create a Document Translation resource
Document Translation supports [single-service access][single_service] only.
To access the service, create a Translator resource.

You can create the resource using

**Option 1:** [Azure Portal][azure_portal_create_DT_resource]

**Option 2:** [Azure CLI][azure_cli_create_DT_resource].
Below is an example of how you can create a Document Translation resource using the CLI:

```bash
# Create a new resource group to hold the document translation resource -
# if using an existing resource group, skip this step
az group create --name my-resource-group --location westus2
```

```bash
# Create document translation
az cognitiveservices account create \
    --name document-translation-resource \
    --custom-domain document-translation-resource \
    --resource-group my-resource-group \
    --kind TextTranslation \
    --sku S1 \
    --location westus2 \
    --yes
```

### Authenticate the client
In order to interact with the Document Translation service, you will need to create an instance of a client.
An **endpoint** and **credential** are necessary to instantiate the client object.


#### Looking up the endpoint
You can find the endpoint for your Document Translation resource using the
[Azure Portal][azure_portal_get_endpoint].

> Note that the service requires a custom domain endpoint. Follow the instructions in the above link to format your endpoint:
> https://{NAME-OF-YOUR-RESOURCE}.cognitiveservices.azure.com/

#### Get the API key

The API key can be found in the Azure Portal or by running the following Azure CLI command:

```az cognitiveservices account keys list --name "resource-name" --resource-group "resource-group-name"```

#### Create the client with AzureKeyCredential

To use an [API key][cognitive_authentication_api_key] as the `credential` parameter,
pass the key as a string into an instance of [AzureKeyCredential][azure-key-credential].

```python
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.document import DocumentTranslationClient

endpoint = "https://<resource-name>.cognitiveservices.azure.com/"
credential = AzureKeyCredential("<api_key>")
document_translation_client = DocumentTranslationClient(endpoint, credential)
```

## Key concepts

The Document Translation service requires that you upload your files to an Azure Blob Storage source container and provide
a target container where the translated documents can be written. SAS tokens to the containers (or files) are used to
access the documents and create the translated documents in the target container. Additional information about setting this up can be found in
the service documentation:

- [Set up Azure Blob Storage containers][source_containers] with your documents
- Optionally apply [glossaries][glossary] or a [custom model for translation][custom_model]
- Generate [SAS tokens][sas_token] to your containers (or files) with the appropriate [permissions][sas_token_permissions]


### DocumentTranslationClient

Interaction with the Document Translation client library begins with an instance of the `DocumentTranslationClient`.
The client provides operations for:

 - Creating a translation job to translate documents in your source container(s) and write results to you target container(s).
 - Checking the status of individual documents in the translation job and monitoring each document's progress.
 - Enumerating all past and current translation jobs with the option to wait until the job(s) finish.
 - Identifying supported glossary and document formats.

### Translation Input

To create a translation job, pass a list of `DocumentTranslationInput` into the `create_translation_job` client method.
Constructing a `DocumentTranslationInput` requires that you pass the SAS URLs to your source and target containers (or files)
and the target language(s) for translation.

A single source container with documents can be translated to many different languages:

```python
from azure.ai.translation.document import DocumentTranslationInput, TranslationTarget

my_input = [
    DocumentTranslationInput(
        source_url="<sas_url_to_source>",
        targets=[
            TranslationTarget(target_url="<sas_url_to_target_fr>", language_code="fr"),
            TranslationTarget(target_url="<sas_url_to_target_de>", language_code="de")
        ]
    )
]
```

Or multiple different sources can be provided each with their own targets.

```python
from azure.ai.translation.document import DocumentTranslationInput, TranslationTarget

my_input = [
    DocumentTranslationInput(
        source_url="<sas_url_to_source_A>",
        targets=[
            TranslationTarget(target_url="<sas_url_to_target_fr>", language_code="fr"),
            TranslationTarget(target_url="<sas_url_to_target_de>", language_code="de")
        ]
    ),
    DocumentTranslationInput(
        source_url="<sas_url_to_source_B>",
        targets=[
            TranslationTarget(target_url="<sas_url_to_target_fr>", language_code="fr"),
            TranslationTarget(target_url="<sas_url_to_target_de>", language_code="de")
        ]
    ),
    DocumentTranslationInput(
        source_url="<sas_url_to_source_C>",
        targets=[
            TranslationTarget(target_url="<sas_url_to_target_fr>", language_code="fr"),
            TranslationTarget(target_url="<sas_url_to_target_de>", language_code="de")
        ]
    )
]
```

> Note: the target_url for each target language must be unique.

See the service documentation for all [supported languages][supported_languages].

### Return value

There are primarily two types of return values when checking on the result of a translation job - `JobStatusResult` and `DocumentStatusResult`.
* A `JobStatusResult` will contain the details of the entire job, such as it's status, ID, any errors, and status summaries of the documents in the job.
* A `DocumentStatusResult` will contain the details of an individual document, such as it's status, translation progress, any errors,
and the URLs to the source document and translated document.


## Troubleshooting

### General
Document Translation client library will raise exceptions defined in [Azure Core][azure_core_exceptions].

### Logging
This library uses the standard
[logging][python_logging] library for logging.

Basic information about HTTP sessions (URLs, headers, etc.) is logged at `INFO` level.

Detailed `DEBUG` level logging, including request/response bodies and **unredacted**
headers, can be enabled on the client or per-operation with the `logging_enable` keyword argument.

See full SDK logging documentation with examples [here][sdk_logging_docs].

### Optional Configuration

Optional keyword arguments can be passed in at the client and per-operation level.
The azure-core [reference documentation][azure_core_ref_docs]
describes available configurations for retries, logging, transport protocols, and more.

### Additional documentation

For more extensive documentation on Azure Cognitive Services Document Translation, see the [Document Translation documentation][python-dt-product-docs] on docs.microsoft.com.

## Contributing
This project welcomes contributions and suggestions. Most contributions require you to agree to a Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us the rights to use your contribution. For details, visit [cla.microsoft.com][cla].

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct][code_of_conduct]. For more information see the [Code of Conduct FAQ][coc_faq] or contact [opencode@microsoft.com][coc_contact] with any additional questions or comments.

<!-- LINKS -->

[python-dt-src]: https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/translation/azure-ai-translation-document/azure/ai/translation/document
[python-dt-pypi]: https://aka.ms/azsdk/python/texttranslation/pypi
[python-dt-product-docs]: https://docs.microsoft.com/azure/cognitive-services/translator/document-translation/overview
[python-dt-ref-docs]: https://aka.ms/azsdk/python/documenttranslation/docs
[python-dt-samples]: https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/translation/azure-ai-translation-document/samples

[azure_subscription]: https://azure.microsoft.com/free/
[DT_resource]: https://docs.microsoft.com/azure/cognitive-services/translator/document-translation/get-started-with-document-translation?tabs=python
[single_service]: https://docs.microsoft.com/azure/cognitive-services/cognitive-services-apis-create-account?tabs=singleservice%2Cwindows
[pip]: https://pypi.org/project/pip/
[azure_portal_create_DT_resource]: https://ms.portal.azure.com/#create/Microsoft.CognitiveServicesTextTranslation
[azure_cli_create_DT_resource]: https://docs.microsoft.com/azure/cognitive-services/cognitive-services-apis-create-account-cli?tabs=windows
[azure-key-credential]: https://aka.ms/azsdk/python/core/azurekeycredential
[supported_languages]: https://docs.microsoft.com/azure/cognitive-services/translator/language-support#translate
[source_containers]: https://docs.microsoft.com/azure/cognitive-services/translator/document-translation/get-started-with-document-translation?tabs=csharp#create-your-azure-blob-storage-containers
[custom_model]: https://docs.microsoft.com/azure/cognitive-services/translator/custom-translator/quickstart-build-deploy-custom-model
[glossary]: https://docs.microsoft.com/azure/cognitive-services/translator/document-translation/overview#supported-glossary-formats
[sas_token]: https://docs.microsoft.com/azure/cognitive-services/translator/document-translation/create-sas-tokens?tabs=Containers#create-your-sas-tokens-with-azure-storage-explorer
[sas_token_permissions]: https://docs.microsoft.com/azure/cognitive-services/translator/document-translation/get-started-with-document-translation?tabs=csharp#create-sas-access-tokens-for-document-translation
[azure_storage_blob]: https://pypi.org/project/azure-storage-blob/

[azure_core_ref_docs]: https://aka.ms/azsdk/python/core/docs
[azure_core_exceptions]: https://aka.ms/azsdk/python/core/docs#module-azure.core.exceptions
[python_logging]: https://docs.python.org/3/library/logging.html
[azure_cli_endpoint_lookup]: https://docs.microsoft.com/cli/azure/cognitiveservices/account?view=azure-cli-latest#az-cognitiveservices-account-show
[azure_portal_get_endpoint]: https://docs.microsoft.com/azure/cognitive-services/translator/document-translation/get-started-with-document-translation?tabs=csharp#get-your-custom-domain-name-and-subscription-key
[cognitive_authentication_api_key]: https://docs.microsoft.com/azure/cognitive-services/translator/document-translation/get-started-with-document-translation?tabs=csharp#get-your-subscription-key

[sdk_logging_docs]: https://docs.microsoft.com/azure/developer/python/azure-sdk-logging

[sample_authentication]: https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/translation/azure-ai-translation-document/samples/sample_authentication.py
[sample_authentication_async]: https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/translation/azure-ai-translation-document/samples/async_samples/sample_authentication_async.py
[sample_create_translation_job]: https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/translation/azure-ai-translation-document/samples/sample_create_translation_job.py
[sample_create_translation_job_async]: https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/translation/azure-ai-translation-document/samples/async_samples/sample_create_translation_job_async.py
[sample_check_document_statuses]: https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/translation/azure-ai-translation-document/samples/sample_check_document_statuses.py
[sample_check_document_statuses_async]: https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/translation/azure-ai-translation-document/samples/async_samples/sample_check_document_statuses_async.py
[sample_list_all_submitted_jobs]: https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/translation/azure-ai-translation-document/samples/sample_list_all_submitted_jobs.py
[sample_list_all_submitted_jobs_async]: https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/translation/azure-ai-translation-document/samples/async_samples/sample_list_all_submitted_jobs_async.py
[sample_translation_with_glossaries]: https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/translation/azure-ai-translation-document/samples/sample_translation_with_glossaries.py
[sample_translation_with_glossaries_async]: https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/translation/azure-ai-translation-document/samples/async_samples/sample_translation_with_glossaries_async.py
[sample_translation_with_azure_blob]: https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/translation/azure-ai-translation-document/samples/sample_translation_with_azure_blob.py
[sample_translation_with_azure_blob_async]: https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/translation/azure-ai-translation-document/samples/async_samples/sample_translation_with_azure_blob_async.py

[cla]: https://cla.microsoft.com
[code_of_conduct]: https://opensource.microsoft.com/codeofconduct/
[coc_faq]: https://opensource.microsoft.com/codeofconduct/faq/
[coc_contact]: mailto:opencode@microsoft.com
