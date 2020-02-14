# Form Recognizer

## Prebuilt

### Prebuilt: Form Recognizer Client
```python
from azure.ai.formrecognizer import FormRecognizerClient

client = FormRecognizerClient(endpoint: str, credential: Union[FormRecognizerApiKeyCredential, TokenCredential])

# Content-type of document is determined in method
# These are LRO, but don't return the poller object to user. Operation will block until result is returned.
client.extract_receipt(document: Any, **kwargs) -> ExtractedReceipt
client.extract_layout(document: Any, **kwargs) -> List[ExtractedTables]
```

### Prebuilt: Receipt Models
```python
# doesn't include errors list -- need to understand that story
class ExtractedReceipt:
    receipt_items: List[ReceiptItem]
    merchant_address: FieldValue
    merchant_name: FieldValue
    merchant_phone_number: FieldValue
    receipt_type: str
    subtotal: FieldValue
    tax: FieldValue
    tip: FieldValue
    total: FieldValue
    transaction_date: FieldValue
    transaction_time: FieldValue

class ReceiptItem:
    name: str
    quantity: int
    total_price: float
    bounding_box: List[int]
    confidence: float
    raw_fields: List[ExtractedLine]

class FieldValue:
    bounding_box: List[int]
    confidence: float
    page_number: int
    value: str
    raw_fields: List[ExtractedLine]

class ExtractedLine:
    bounding_box: List[int]
    language: str
    text: str
    words: List[ExtractedWord]

class ExtractedWord:
    bounding_box: List[int]
    confidence: float
    text: str
```

### Prebuilt: Receipt Sample
```python
from azure.ai.formrecognizer import FormRecognizerClient, FormRecognizerApiKeyCredential

client = FormRecognizerClient(endpoint, FormRecognizerApiKeyCredential(credential))

document = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/contoso-allinone.jpg"
result = client.extract_receipt(document)

# Access the labeled data
print("Receipt contained the following values: ")
print("ReceiptType: {}").format(result.receipt_type)
print("MerchantName: {}").format(result.merchant_name.value)
print("MerchantAddress: {}").format(result.merchant_address.value)
print("MerchantPhoneNumber: {}").format(result.merchant_phone_number.value)
print("TransactionDate: {}").format(result.transaction_date.value)
print("TransactionTime: {}").format(result.transaction_time.value)
for item in result.receipt_items:
    print("Item Name: {}").format(item.name)
    print("Item Quantity: {}").format(item.quantity)
    print("Item Price: {}").format(item.total_price)


# Access the raw OCR result for merchant name
for line in result.merchant_name.raw_fields:
    print("Line contains: {}").format(line.text)
    for word in line.words:
        print("Word: {}").format(word.text)
```

### Prebuilt: Layout Models

```python
class ExtractedTables:
    table: List[List[TableCell]]  # table[row][col] = TableCell
    columns: int
    page_number: int
    rows: int

class TableCell:
    bounding_box: List[int]
    column_index: int
    column_span: int
    confidence: float
    is_footer: bool
    is_header: bool
    row_index: int
    row_span: int
    text: str
    raw_fields: List[ExtractedLine]

class ExtractedLine:
    bounding_box: List[int]
    language: str
    text: str
    words: List[ExtractedWord]

class ExtractedWord:
    bounding_box: List[int]
    confidence: float
    text: str
```

### Prebuilt: Layout Sample

```python
import pandas as pd
from azure.ai.formrecognizer import FormRecognizerClient, FormRecognizerApiKeyCredential

client = FormRecognizerClient(endpoint, FormRecognizerApiKeyCredential(credential))

document = "https://i.stack.imgur.com/1FyIg.png"
result = client.extract_layout(document)

dftable = pd.DataFrame(result.table)
print(dftable)
```

## Custom

### Custom: Custom Model Client
```python
from azure.ai.formrecognizer import CustomModelClient, FormRecognizerApiKeyCredential

client = CustomModelClient(endpoint: str, credential: Union[FormRecognizerApiKeyCredential, TokenCredential])

# include_text_details: True moves to kwargs

client.begin_labeled_training(
    source: str, source_prefix_filter: str, include_sub_folders: bool=False
) -> LROPoller -> LabeledCustomModel

client.begin_unlabeled_training(
    source: str, source_prefix_filter: str, include_sub_folders: bool=False
) -> LROPoller -> CustomModel

# Content-type determined in method
client.analyze_document(document: Any, model_id: str,) -> LROPoller -> ExtractedDocument

# Content-type determined in method
client.extract_labeled_fields(document: Any, model_id: str) -> LROPoller -> LabeledExtractedDocument

client.list_custom_models() -> ItemPaged[ModelInfo]

client.get_models_summary() -> ModelsSummary

client.delete_custom_model(model_id: str) -> None

# analyze form methods might need to return lists if capable of analyzing more than one page
```

### Custom: Custom Models Unlabeled
```python
# Training ---------------------------------------------------
class CustomModel:
    model_id: str
    status: str
    created_date_time: ~datetime.datetime
    last_updated_date_time: ~datetime.datetime
    extracted_fields: dict[str, list[str]]
    train_result: UnlabeledTrainResult

class UnlabeledTrainResult:
    training_documents: List[TrainingDocumentInfo]
    average_model_accuracy: float
    errors: List[ErrorInformation]

class TrainingDocumentInfo:
    document_name: str
    pages: int
    errors: List[ErrorInformation]
    status: str

class ErrorInformation:
    code: str
    message: str

# Analyze ---------------------------------------------------
class ExtractedDocument:
    key_value_pairs: List[KeyValuePair]
    tables: List[ExtractedTables]
    page_number: int
    cluster_id: int

class KeyValuePair:
    key: TextValue
    value: TextValue
    confidence: float

class TextValue:
    text: str
    bounding_box: List[float]
    raw_fields: List[ExtractedLine]

class ExtractedLine:
    bounding_box: List[int]
    language: str
    text: str
    words: List[ExtractedWord]

class ExtractedWord:
    bounding_box: List[int]
    confidence: float
    text: str
```

### Custom: Custom Models Labeled
```python
# Training ---------------------------------------------------
class LabeledCustomModel:
    model_id: str
    status: str
    created_date_time: ~datetime.datetime
    last_updated_date_time: ~datetime.datetime
    train_result: LabeledTrainResult

class LabeledTrainResult:
    training_documents: List[TrainingDocumentInfo]
    fields: List[FieldNames]
    average_model_accuracy: float
    errors: List[ErrorInformation]

class TrainingDocumentInfo:
    document_name: str
    pages: int
    status: str

class FieldNames:
    field_name: str
    accuracy: float

class ErrorInformation:
    code: str
    message: str

# Analyze ---------------------------------------------------
class LabeledExtractedDocument:
    labels: List[Dict{"user label": FieldValue}]
    tables: List[ExtractedTables]
    page_number: int

class FieldValue:
    bounding_box: List[int]
    confidence: float
    value: str
    raw_field: List[ExtractedLine]

class ExtractedLine:
    bounding_box: List[int]
    language: str
    text: str
    words: List[ExtractedWord]

class ExtractedWord:
    bounding_box: List[int]
    confidence: float
    text: str
```

### Custom: List/Get/Delete Models
```python
class ModelInfo:
    model_id: str
    status: str
    created_date_time: ~datetime.datetime
    last_updated_date_time: ~datetime.datetime

class ModelsSummary:
    count: int
    limit: int
    last_updated_date_time: ~datetime.datetime
```


### Custom: Custom Training Samples

#### Custom: Train and Analyze without labels
```python
from azure.ai.formrecognizer import FormRecognizerClient

client = FormRecognizerClient(endpoint=endpoint, credential=key)

blob_sas_url = "xxxxx"  # training documents uploaded to blob storage
poller = client.begin_unlabeled_training(blob_sas_url)

# ...check poller status...

custom_model = poller.result()
print(custom_model.model_id)
print(custom_model.extracted_fields) # list of fields OCR found on the from form

blob_sas_url = "xxxxx"  # document to analyze uploaded to blob storage
poller = client.analyze_document(blob_sas_url, model_id="xxx")

# ... check poller status...

result = poller.result()

for form in result.key_value_pairs:
    print(form.key.text, form.value.text)
```

#### Custom: Train and Analyze with labels
```python
from azure.ai.formrecognizer import FormRecognizerClient

client = FormRecognizerClient(endpoint=endpoint, credential=key)

blob_sas_url = "xxxxx"  # training documents uploaded to blob storage
poller = client.begin_labeled_training(blob_sas_url)

# ...check poller status...

custom_model = poller.result()
print(custom_model.model_id)
print(custom_model.train_result.fields)  # list of fields / accuracy

blob_sas_url = "xxxxx"  # document to analyze uploaded to blob storage
poller = client.extract_labeled_fields(blob_sas_url, model_id="xxx")

# ... check poller status...

result = poller.result()

for form in result.labels:
    for label, text in form.items():
        print("{}: {}".format(label, text.value))
```

#### Custom: List custom models
```python
from azure.ai.formrecognizer import FormRecognizerClient

client = FormRecognizerClient(endpoint=endpoint, credential=key)
custom_models = list(client.list_custom_models())
for model in custom_models:
    print(model.model_id, model.status)
```

#### Custom: Get models summary
```python
from azure.ai.formrecognizer import FormRecognizerClient

client = FormRecognizerClient(endpoint=endpoint, credential=key)
summary = client.get_models_summary()

print("Number of models: {}".format(summary.count))
print("Max number of models that can be trained with this subscription: {}".format(summary.limit))
print("Datetime when summary was updated: {}".format(summary.last_updated_date_time))
```

#### Custom: Delete custom model
```python
from azure.ai.formrecognizer import FormRecognizerClient

client = FormRecognizerClient(endpoint=endpoint, credential=key)
client.delete_custom_model(model_id="xxxxx")
```
