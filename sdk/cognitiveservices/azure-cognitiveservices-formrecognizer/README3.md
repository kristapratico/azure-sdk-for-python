# Form Recognizer Design Overview

The Form Recognizer client library provides two clients to interact with the service: `FormRecognizerClient` and 
`CustomFormClient`, which can be imported from the `azure.ai.formrecognizer` namespace. The asynchronous clients 
can be imported from the `azure.ai.formrecognizer.aio` namespace.

`FormRecognizerClient` provides methods for interacting with the prebuilt models (receipt and layout).
`CustomFormClient` provides the methods for training custom models to analyze forms.

Authentication is achieved by passing an instance of `CognitiveKeyCredential("<api_key>")` to the client,
or by providing a token credential from `azure.identity` to use Azure Active Directory.

## Prebuilt

The prebuilt models are accessed through the `FormRecognizerClient`. The input form or document can be passed as a 
string url to the image, or as a file stream. The SDK will determine content-type and send the appropriate header. 

The `begin_extract_receipt` method returns an `ExtractedReceipt` with hardcoded receipt fields.
The `begin_extract_layout` method returns the extracted tables in a tabular format such that the user can
index into a specific row or column and easily integrate with other Python libraries.

If the keyword argument `include_text_details=True` is passed in, the `raw_` attributes will be populated with the
raw OCR result for each value/cell.

### Prebuilt: Form Recognizer Client
```python
from azure.ai.formrecognizer import FormRecognizerClient

client = FormRecognizerClient(endpoint: str, credential: Union[CognitiveKeyCredential, TokenCredential])

# Content-type of document is determined in method
client.begin_extract_receipt(document: Any, **kwargs) -> LROPoller -> List[ExtractedReceipt]

client.begin_extract_layout(document: Any, **kwargs) -> LROPoller -> List[ExtractedPage]
```

### Prebuilt: Receipt Models
```python
class ExtractedReceipt:
    receipt_items: List[ReceiptItem]
    merchant_address: str
    merchant_name: str
    merchant_phone_number: str
    receipt_type: str
    subtotal: float
    tax: float
    tip: float
    total: float
    transaction_date: str
    transaction_time: str
    fields: RawReceiptData

class ReceiptItem:
    name: str
    quantity: int
    total_price: float

class RawReceiptData:
    receipt_items: List[RawReceiptItem]
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

class RawReceiptItem:
    name: str
    quantity: int
    total_price: float
    bounding_box: List[float]
    confidence: float
    raw_field: List[ExtractedLine]

class FieldValue:
    value: Union[str, float, int]
    bounding_box: List[float]
    confidence: float
    raw_field: List[ExtractedLine]

class ExtractedLine:
    text: str
    bounding_box: List[float]
    language: str
    words: List[ExtractedWord]

class ExtractedWord:
    text: str
    bounding_box: List[float]
    confidence: float
```

### Prebuilt: Receipt Sample
```python
from azure.ai.formrecognizer import FormRecognizerClient

client = FormRecognizerClient(endpoint, credential)

document = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/contoso-allinone.jpg"
poller = client.begin_extract_receipt(document)
receipt = poller.result()
result = receipt[0]

print("Receipt contained the following values: ")
print("ReceiptType: {}").format(result.receipt_type)
print("MerchantName: {}").format(result.merchant_name)
print("MerchantAddress: {}").format(result.merchant_address)
print("MerchantPhoneNumber: {}").format(result.merchant_phone_number)
print("TransactionDate: {}").format(result.transaction_date)
print("TransactionTime: {}").format(result.transaction_time)
for item in result.receipt_items:
    print("Item Name: {}").format(item.name)
    print("Item Quantity: {}").format(item.quantity)
    print("Item Price: {}").format(item.total_price)
print("Subtotal: {}").format(result.subtotal)
print("Tax: {}").format(result.tax)
print("Tip: {}").format(result.tip)
print("Total: {}").format(result.total)
```

### Prebuilt: Layout Models

```python
class ExtractedPage:
    tables: List[ExtractedTable]
    page_number: int

class ExtractedTable: 
    List[List[TableCell]]
    row_count: int
    column_count: int

class TableCell:
    text: str
    column_index: int
    column_span: int
    confidence: float
    is_footer: bool
    is_header: bool
    row_index: int
    row_span: int
    bounding_box: List[float]
    raw_field: List[ExtractedLine]

class ExtractedLine:
    text: str
    bounding_box: List[float]
    language: str
    words: List[ExtractedWord]

class ExtractedWord:
    text: str
    bounding_box: List[float]
    confidence: float
```

### Prebuilt: Layout Sample

```python
import pandas as pd
from azure.ai.formrecognizer import FormRecognizerClient

client = FormRecognizerClient(endpoint, credential)

document = "https://i.stack.imgur.com/1FyIg.png"
poller = client.begin_extract_layout(document)
result = poller.result()

dftable = pd.DataFrame(result[0].tables[0])
print(dftable)
```

## Custom

The `CustomFormClient` provides all the operations necessary for training a custom model, analyzing a form with a 
custom model, and managing a user's custom models on their account.

The user can choose to train with or without labels using the methods `begin_labeled_training` or `begin_training`. 
Both methods take as input a blob SAS url to the documents to use for training. Each training method will return a
poller object which is used to get the training result.

A custom model can be used to analyze forms using the `begin_analyze_form` or `begin_extract_labeled_fields` methods.
The `model_id` from the training result is passed into the methods, along with the input form to analyze (content-type
is determined internally). Both methods return a poller object which is used to get the result object.

In order for the user to manage their custom models, a few methods are available to list custom models, delete a model,
and get a models summary for the account.

### Custom: Custom Form Client
```python
from azure.ai.formrecognizer import CustomFormClient

client = CustomFormClient(endpoint: str, credential: Union[CognitiveKeyCredential, TokenCredential])

client.begin_labeled_training(
    source: str, source_prefix_filter: str, include_sub_folders: bool=False
) -> LROPoller -> LabeledCustomModel

client.begin_training(
    source: str, source_prefix_filter: str, include_sub_folders: bool=False
) -> LROPoller -> CustomModel

# Content-type determined in method
client.begin_analyze_form(form: Any, model_id: str,) -> LROPoller -> List[ExtractedPage]

# Content-type determined in method
client.begin_extract_labeled_fields(form: Any, model_id: str) -> LROPoller -> List[LabeledExtractedPage]

client.list_custom_models() -> ItemPaged[ModelInfo]

client.get_models_summary() -> ModelsSummary

client.delete_custom_model(model_id: str) -> None
```

### Custom: Custom Models Unlabeled
```python
# Training ---------------------------------------------------
class CustomModel:
    model_id: str
    status: str
    created_date_time: ~datetime.datetime
    last_updated_date_time: ~datetime.datetime
    form_clusters: dict[str, list[str]]
    train_result: TrainResult

class TrainResult:
    training_documents: List[TrainingDocumentInfo]
    average_model_accuracy: float
    training_errors: List[ErrorInformation]

class TrainingDocumentInfo:
    document_name: str
    pages: int
    document_errors: List[ErrorInformation]
    status: str

class ErrorInformation:
    code: str
    message: str

# Analyze ---------------------------------------------------
class ExtractedPage:
    fields: List[ExtractedField]
    tables: List[ExtractedTable]
    page_number: int
    cluster_id: int

class ExtractedField:
    name: TextValue
    value: TextValue
    confidence: float

class TextValue:
    text: str
    bounding_box: List[float]
    raw_field: List[ExtractedLine]

class ExtractedLine:
    text: str
    bounding_box: List[float]
    language: str
    words: List[ExtractedWord]

class ExtractedWord:
    text: str
    bounding_box: List[float]
    confidence: float
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
    training_errors: List[ErrorInformation]

class TrainingDocumentInfo:
    document_name: str
    pages: int
    document_errors: List[ErrorInformation]
    status: str

class FieldNames:
    field_name: str
    accuracy: float

class ErrorInformation:
    code: str
    message: str

# Analyze ---------------------------------------------------
class LabeledExtractedPage:
    fields: List[ExtractedLabel]
    tables: List[ExtractedTable]
    page_number: int

class ExtractedLabel:
    name: str
    value: LabelValue

class LabelValue:
    text: str
    bounding_box: List[float]
    confidence: float
    raw_field: List[ExtractedLine]

class ExtractedLine:
    text: str
    bounding_box: List[float]
    language: str
    words: List[ExtractedWord]

class ExtractedWord:
    text: str
    bounding_box: List[float]
    confidence: float
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
from azure.ai.formrecognizer import CustomFormClient

client = CustomFormClient(endpoint=endpoint, credential=credential)

blob_sas_url = "xxxxx"  # training documents uploaded to blob storage
poller = client.begin_training(blob_sas_url)
custom_model = poller.result()

print(custom_model.model_id)
print(custom_model.form_clusters) # extracted fields / clustered

blob_sas_url = "xxxxx"  # form to analyze uploaded to blob storage
poller = client.begin_analyze_form(blob_sas_url, model_id=custom_model.model_id)
result = poller.result()

for page in result:
    print("Page: {}".format(page.page_number))
    for field in page.fields:
        print(field.name.text, field.value.text)
```

#### Custom: Train and Analyze with labels
```python
from azure.ai.formrecognizer import CustomFormClient

client = CustomFormClient(endpoint=endpoint, credential=credential)

blob_sas_url = "xxxxx"  # training documents uploaded to blob storage
poller = client.begin_labeled_training(blob_sas_url)
custom_model = poller.result()

print(custom_model.model_id)
print(custom_model.train_result.fields)  # list of fields / accuracy

blob_sas_url = "xxxxx"  # form to analyze uploaded to blob storage
poller = client.begin_extract_labeled_fields(blob_sas_url, model_id=custom_model.model_id)
result = poller.result()

for page in result:
    print("Page: {}".format(page.page_number))
    for field in page.fields:
        print(field.name, field.value.text)
```

#### Custom: List custom models
```python
from azure.ai.formrecognizer import CustomFormClient

client = CustomFormClient(endpoint=endpoint, credential=credential)
custom_models = list(client.list_custom_models())
for model in custom_models:
    print(model.model_id, model.status)
```

#### Custom: Get models summary
```python
from azure.ai.formrecognizer import CustomFormClient

client = CustomFormClient(endpoint=endpoint, credential=credential)
summary = client.get_models_summary()

print("Number of models: {}".format(summary.count))
print("Max number of models that can be trained with this subscription: {}".format(summary.limit))
print("Datetime when summary was updated: {}".format(summary.last_updated_date_time))
```

#### Custom: Delete custom model
```python
from azure.ai.formrecognizer import CustomFormClient

client = CustomFormClient(endpoint=endpoint, credential=credential)
client.delete_custom_model(model_id="xxxxx")
```
