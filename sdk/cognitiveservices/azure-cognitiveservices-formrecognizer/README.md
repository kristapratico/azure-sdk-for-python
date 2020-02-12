### Form Recognizer

## Prebuilt

Prebuilt: Form Recognizer Client
```python
# should this come from a different namespace?
# How will this work with the poller, polls internally?
from azure.ai.formrecognizer import FormRecognizerClient

client = FormRecognizerClient(endpoint, credential)  # FormRecognizerApiKeyCredential or TokenCredential

# Content-type of document is determined in method
client.extract_receipt(document: Any, include_text_details: bool=False, **kwargs) -> ReceiptResult

# Content-type of document is determined in method
client.extract_layout(document: Any, **kwargs) -> LayoutResult
```

Prebuilt: Receipt Models
```python
class ReceiptResult:
    receipt: Dict{ExtractedReceipt.key: FieldValue.value}
    receipt_details: ExtractedReceipt
    text_details: List[ExtractedPage]

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

# Alternatively

print("Receipt contained the following values: ")
print("ReceiptType: {}").format(result.receipt_details.receipt_type)
print("MerchantName: {}").format(result.receipt_details.merchant_name.value)
print("MerchantAddress: {}").format(result.receipt_details.merchant_address.value)
print("MerchantPhoneNumber: {}").format(result.receipt_details.merchant_phone_number.value)
print("TransactionDate: {}").format(result.receipt_details.transaction_date.value)
print("TransactionTime: {}").format(result.receipt_details.transaction_time.value)

for item in result.receipt_details.items():
    print("Item Name: {}").format(item.name)
    print("Item Quantity: {}").format(item.quantity)
    print("Item Price: {}").format(item.total_price)

print("Subtotal: {}").format(result.receipt_details.subtotal)
print("Tax: {}").format(result.receipt_details.tax)
print("Tip: {}").format(result.receipt_details.tip)
print("Total: {}").format(result.receipt_details.total)

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
    extracted_tables : List[ExtractedTables]
    text_details : List[ExtractedPage]

class ExtractedTables:
    cells: List[TableCell]
    columns: int
    page_number: int
    rows: int

class TableCell:
    bounding_box: List[int]
    column_index: int
    column_span: int
    confidence: score
    is_footer: bool
    is_header: bool
    row_index: int
    row_span: int
    text: str
```

Prebuilt: Layout Sample

```python
from azure.ai.formrecognizer import FormRecognizerClient, FormRecognizerApiKeyCredential

client = FormRecognizerClient(endpoint, FormRecognizerApiKeyCredential(credential))

document = "https://i.stack.imgur.com/1FyIg.png"
result = client.extract_layout(document)

for table in result.extracted_tables:
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
from azure.ai.formrecognizer import CustomModelClient

client = CustomModelClient()
```


