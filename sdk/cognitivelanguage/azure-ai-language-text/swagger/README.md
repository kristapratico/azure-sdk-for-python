# Text Analytics for Python

To generate this file, simply type

```
autorest swagger/README.md --python-sdks-folder=<path to the root directory of your azure-sdk-for-python clone>
```

We automatically hardcode in that this is `python`.

## Basic

```yaml
license-header: MICROSOFT_MIT_NO_VERSION
add-credential: true
payload-flattening-threshold: 2
package-name: azure-ai-language-text
clear-output-folder: true
credential-scopes: https://cognitiveservices.azure.com/.default
no-namespace-folders: true
python: true
modelerfour: 
  lenient-model-deduplication: true
```

## Release 2022-02-01-preview

These settings apply only when `--tag=release_2022_02_01_preview` is specified on the command line.

```yaml $(tag) == 'release_2022_02_01_preview'
input-file: https://raw.githubusercontent.com/Azure/azure-rest-api-specs/b1f3b5cea725a5f2fa2af06e20c5b5fd9f39ec20/specification/cognitiveservices/data-plane/Language/preview/2022-02-01-preview/textanalytics.json
namespace: azure.ai.language.text
output-folder: $(python-sdks-folder)/cognitivelanguage/azure-ai-language-text/azure/ai/language/text/_generated/
```
