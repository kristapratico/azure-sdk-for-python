

Prebuilt: Receipt Client
```python
# should this come from a different namespace?
# How will this work with the poller, polls internally?
from azure.ai.formrecognizer import ReceiptExtractionClient

client = ReceiptExtractionClient(endpoint, credential)  # FormRecognizerApiKeyCredential or TokenCredential

# Content-type of document is determined in method
client.extract_receipt(document: Any, include_text_details: bool=False, **kwargs) -> ReceiptResult

# For getting the cached result without calling extract_receipt() 
# Does this mean that extract_receipt() needs to return the result location as well?
client.get_receipt_result(result_location: str) -> ReceiptResult
```

Prebuilt: Receipt Models
```python
class ReceiptResult:
    receipt: ExtractedReceipt
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
from azure.ai.formrecognizer import ReceiptExtractionClient, FormRecognizerApiKeyCredential

client = ReceiptExtractionClient(endpoint, FormRecognizerApiKeyCredential(credential))

document = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/contoso-allinone.jpg"
result = client.extract_receipt(document)

# Access the labeled data
print("Receipt contained the following values: ")

print("ReceiptType: {}").format(result.receipt.receipt_type)
print("MerchantName: {}").format(result.receipt.merchant_name.value)
print("MerchantAddress: {}").format(result.receipt.merchant_address.value)
print("MerchantPhoneNumber: {}").format(result.receipt.merchant_phone_number.value)
print("TransactionDate: {}").format(result.receipt.transaction_date.value)
print("TransactionTime: {}").format(result.receipt.transaction_time.value)

for item in result.receipt.items:
    print("Item Name: {}").format(item.name)
    print("Item Quantity: {}").format(item.quantity)
    print("Item Price: {}").format(item.total_price)

print("Subtotal: {}").format(result.receipt.subtotal)
print("Tax: {}").format(result.receipt.tax)
print("Tip: {}").format(result.receipt.tip)
print("Total: {}").format(result.receipt.total)

# Access the raw OCR result
for page in result.text_details:
    print("Page number: {}").format(page.page_number)
    for line in page.lines:
        print("Line contains: {}").format(line.text)
        for word in line.words:
            print("Word: {}").format(word.text)
```

Prebuilt: Layout Client

```python
from azure.ai.formrecognizer import LayoutExtractionClient, FormRecognizerApiKeyCredential

client = LayoutExtractionClient(endpoint, FormRecognizerApiKeyCredential(credential))

# Content-type of document is determined in method
client.extract_layout(document: Any, **kwargs) -> LayoutResult

# Get cached result without calling extract_layout()
client.get_layout_result(result_location: str) -> LayoutResult
```

Prebuilt: Layout Models

```python
class LayoutResult:
    extracted_tables : List[ExtractedTables]
    text_details : List[ExtractedPage]

class ExtractedTables:
    cells: List[ExtractedTableCell]
    columns: int
    page_number: int
    rows: int

class ExtractedTableCell:
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
from azure.ai.formrecognizer import LayoutExtractionClient, FormRecognizerApiKeyCredential

client = LayoutExtractionClient(endpoint, FormRecognizerApiKeyCredential(credential))

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