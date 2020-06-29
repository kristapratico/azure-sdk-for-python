
v2.1 introduces SelectionMark which looks like this...

```python
class SelectionMark:
    bounding_box: list[Point]
    confidence: float
    state: SelectionMarkState enum = "selected", "unselected"
```

SelectionMark returns on ReadResult and would become part of our FormPage since a list of SelectionMark are
returned per page:

```python
class FormPage:
    page_number: int
    text_angle: float
    width: float
    height: float
    unit: LengthUnit
    lines: list[FormLine]
    selection_marks: list[SelectionMark]
```

The swagger also shows selectionMark as a new field value type. This would fit into our FieldValue and FieldValueType
accordingly:

```python
# note: doesn't exist in python
class FieldValue:
        public FieldValueType Type { get; }  # type can be "selectionMark"
        public DateTime AsDate();
        public IReadOnlyDictionary<string, FormField> AsDictionary();
        public float AsFloat();
        public long AsInt64();
        public IReadOnlyList<FormField> AsList();
        public string AsPhoneNumber();
        public string AsString();
        public TimeSpan AsTime();
        public FieldValueSelectionMark AsSelectionMark();

class FieldValueSelectionMark(str, Enum):
    selected = "selected"
    unselected = "unselected"
```

In `FormField` we could rename `text` references to `data` or something generic

```python
class FormField:
    label_data: FieldData (was FieldText)
    value_data: FieldData (was FieldText)
    type: str
    name: str
    confidence: float
    value: typed value (python) or FieldValue
```

`FieldData` supports our union type or FormContent base type (.NET style heterogeneous list)

```python
class FieldData(FormContent):
    field_element: Union[FormWord, FormLine, SelectionMark] or IReadOnlyList<FormContent>

class FormContent:
    page_number: int
    bounding_box: BoundingBox
    text: str

class SelectionMark(FormContent):
    confidence: float
    state: SelectionMarkState enum = "selected", "unselected"
```

Another rename we needed to consider is that of `text_content` and `include_text_content` as this now would return 
`SelectionMark`... Suggested renames are `field_elements` and `include_field_elements` to be more general.

Mapping:
How I believe the selection mark properties will map to FormField

For a checkbox like this:

Pizza? [x]

How this would look for unsupervised:

```python
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import FormRecognizerClient

form_recognizer_client = FormRecognizerClient(
    endpoint="<endpoint>", credential=AzureKeyCredential("<key>")
)


poller = form_recognizer_client.begin_recognize_custom_forms_from_url(
    model_id=model_id, form_url="https://myform.com", include_field_elements=True
)
forms = poller.result()
form = forms[0]

for label, field in form.fields.items():
    print(field.name)  # "field-0"
    print(field.value) # "selected"
    print(field.confidence)  # 1.0
    print(field.label_data.text)  # None
    print(field.label_data.bounding_box)  # None
    print(field.label_data.page_number) # None
    print(field.label_data.field_element)  # None
    print(field.value_data.text)  # None
    print(field.value_data.bounding_box)  # BoundingBox
    print(field.value_data.page_number)  # 1
    print(field.value_data.field_element)  # SelectionMark
    print(field.type)  # "selectionMark"
```

How this would look for supervised:

```python
# Training-label "Pizza" was assigned to the checkbox using the labeling tool

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import FormRecognizerClient

form_recognizer_client = FormRecognizerClient(
    endpoint="<endpoint>", credential=AzureKeyCredential("<key>")
)


poller = form_recognizer_client.begin_recognize_custom_forms_from_url(
    model_id=model_id, form_url="https://myform.com", include_field_elements=True
)
forms = poller.result()
form = forms[0]

for label, field in form.fields.items():
    print(field.name)  # "Pizza"
    print(field.value) # "selected"
    print(field.confidence)  # 1.0
    print(field.label_data.text) # None
    print(field.label_data.bounding_box)  # None
    print(field.label_data.page_number) # None
    print(field.label_data.field_element)  # None
    print(field.value_data.text)  # None
    print(field.value_data.bounding_box)  # BoundingBox
    print(field.value_data.page_number)  # 1
    print(field.value_data.field_element)  # SelectionMark
    print(field.type)  # "selectionMark"
```


Link to swagger: https://github.com/Azure/azure-rest-api-specs/blob/8d87a7c7caf59182943b890e7576c04d26642f6f/specification/cognitiveservices/data-plane/FormRecognizer/preview/v2.1-preview.1/FormRecognizer.json