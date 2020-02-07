

```python
from azure.ai.formrecognizer import FormRecognizerClient

client = FormRecognizerClient(endpoint, credential)  # FormRecognizerApiKeyCredential or TokenCredential

# Content-type of document is determined in method
# Returns AnalyzeOperationResult
client.analyze_receipt(document, include_text_details=False, **kwargs)

# Content-type of document is determined in method
# Returns LROPoller, AnalyzeResult
client.analyze_layout(document, **kwargs)
```

or

```python
from azure.ai.formrecognizer import ReceiptClient

client = ReceiptClient(endpoint, credential)  # FormRecognizerApiKeyCredential or TokenCredential

# Content-type of document is determined in method
# Returns LROPoller, AnalyzeResult
client.analyze_receipt(document, include_text_details=False, **kwargs)
```

```python
from azure.ai.formrecognizer import LayoutClient

client = LayoutClient(endpoint, credential)  # FormRecognizerApiKeyCredential or TokenCredential
# Content-type of document is determined in method
# Returns LROPoller, AnalyzeResult
client.analyze_layout(document, **kwargs)
```


```python
from azure.ai.formrecognizer import CustomTrainingClient

client = CustomTrainingClient(endpoint, credential)  # FormRecognizerApiKeyCredential or TokenCredential



```