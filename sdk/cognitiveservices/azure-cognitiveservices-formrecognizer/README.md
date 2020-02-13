### Form Recognizer

## Prebuilt

Prebuilt: Form Recognizer Client
```python
from azure.ai.formrecognizer import FormRecognizerClient

client = FormRecognizerClient(endpoint: str, credential: Union[FormRecognizerApiKeyCredential, TokenCredential])

# Content-type of document is determined in method
client.extract_receipt(document: Any, include_text_details: bool=False, **kwargs) -> ReceiptResult
client.extract_layout(document: Any, **kwargs) -> LayoutResult
```

Prebuilt: Receipt Models
```python
class ReceiptResult:
    receipt: Dict{ExtractedReceipt.key: FieldValue.value}  # Not returned in API, SDK will produce this
    receipt_details: ExtractedReceipt
    text_details: List[ExtractedPage]
    errors: List[ErrorInformation]

class ExtractedReceipt:
    items: List[ReceiptItem]
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

class FieldValue:
    bounding_box: List[int]
    confidence: float
    page_number: int
    value: str

class ExtractedPage:
    language: str
    lines: List[ExtractedLine]
    page_height: float
    page_number: int
    page_width: float
    text_angle: float
    unit: str

class ExtractedLine:
    bounding_box: List[int]
    language: str
    text: str
    words: List[ExtractedWord]

class ExtractedWord:
    bounding_box: List[int]
    confidence: float
    text: str

class ErrorInformation:
    code: str
    message: str
```

Prebuilt: Receipt Sample
```python
from azure.ai.formrecognizer import FormRecognizerClient, FormRecognizerApiKeyCredential

client = FormRecognizerClient(endpoint, FormRecognizerApiKeyCredential(credential))

document = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/contoso-allinone.jpg"
result = client.extract_receipt(document)

# Access the labeled data
print("Receipt contained the following values: ")

for label, value in result.receipt.items():
    print("{}: {}".format(label, value))
 
# Access the raw OCR result
for page in result.text_details:
    print("Page number: {}").format(page.page_number)
    for line in page.lines:
        print("Line contains: {}").format(line.text)
        for word in line.words:
            print("Word: {}").format(word.text)
```

Prebuilt: Layout Models

```python
class LayoutResult:
    tables : List[ExtractedTables]
    text_details : List[ExtractedPage]
    errors : List[ErrorInformation]

class ExtractedTables:
    cells: List[TableCell]
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

class ErrorInformation:
    code: str
    message: str
```

Prebuilt: Layout Sample

```python
from azure.ai.formrecognizer import FormRecognizerClient, FormRecognizerApiKeyCredential

client = FormRecognizerClient(endpoint, FormRecognizerApiKeyCredential(credential))

document = "https://i.stack.imgur.com/1FyIg.png"
result = client.extract_layout(document)

for table in result.tables:
    for cell in table.cells:
        print("Cell text: {}".format(cell.text))
        print("Cell row: {}".format(cell.row_index))
        print("Cell column: {}".format(cell.column_index))
        print("Cell row span: {}".format(cell.row_span)) if cell.row_span else None
        print("Cell column span: {}".format(cell.column_span)) if cell.column_span else None  
```

## Custom

Custom: Custom Model Client

```python
from azure.ai.formrecognizer import CustomModelClient, FormRecognizerApiKeyCredential

client = CustomModelClient(endpoint: str, credential: Union[FormRecognizerApiKeyCredential, TokenCredential])

client.begin_labeled_training(
    source: str, source_prefix_filter: str, include_sub_folders: bool=False, use_label_file: bool=True
) -> LROPoller -> LabeledCustomModel

client.begin_unlabeled_training(
    source: str, source_prefix_filter: str, include_sub_folders: bool=False
) -> LROPoller -> CustomModel

# Content-type determined in method
client.analyze_document(document: Any, model_id: str, include_text_details: bool=False) -> LROPoller -> DocumentResult

# Content-type determined in method
client.extract_labeled_fields(
    document: Any, model_id: str, include_text_details: bool=False
) -> LROPoller -> LabeledDocumentResult

client.list_custom_models() -> ItemPaged[ModelInfo]

client.get_models_summary() -> ModelsSummary

client.delete_custom_model(model_id: str) -> None

```

Custom: Custom Models Unlabeled
```python
class CustomModel:
    model_id: str
    status: str
    created_date_time: ~datetime.datetime
    last_updated_date_time: ~datetime.datetime
    extracted_keys: dict[str, list[str]]
    training_info: TrainInfo

class TrainInfo:
    training_documents: List[TrainingDocumentInfo]
    fields_accuracy: List[AccuracyPerField]
    average_model_accuracy: float
    errors: List[ErrorInformation]

class TrainingDocumentInfo:
    document_name: str
    pages: int
    errors: List[ErrorInformation]
    status: str

class AccuracyPerField:
    field_name: str
    accuracy: float

class ErrorInformation:
    code: str
    message: str

class CustomModelResult:
    result: List[ExtractedDocument]
    text_details: List[ExtractedPage]
    errors: List[ErrorInformation]

class ExtractedDocument:
    result: Dict{KeyValuePair.key.text: KeyValuePair.value.text}  # Not returned in API, SDK will produce this
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

class ExtractedTables:
    cells: List[TableCell]
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
```

Custom: Custom Models Labeled

```python
class LabeledCustomModel:
    


```



```python
class ModelInfo:
    model_id: str
    status: str
    created_date_time: ~datetime.datetime
    last_updated_date_time: ~datetime.datetime
```


Custom: Custom Training Samples

Custom: Train with labels

Custom: Train without labels

Custom: Analyze with custom model - labeled

Custom: Analyze with custom model - unlabeled

Custom: List custom models




Custom: Delete custom model
```python
from azure.ai.formrecognizer import FormRecognizerClient

client = FormRecognizerClient(endpoint=endpoint, credential=key)
client.delete_custom_model(model_id="xxxxx")
```