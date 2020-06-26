
v2.1 introduces SelectionMark which looks like this...

class SelectionMark:
    bounding_box: list[str]
    confidence: float
    state: SelectionMarkState enum = "selected", "unselected"

SelectionMark returns on ReadResult and would become part of our FormPage since a list of SelectionMark are
returned per page:

class FormPage:
    page_number: int
    text_angle: float
    width: float
    height: float
    unit: LengthUnit
    lines: list[FormLine]
    selection_marks: list[SelectionMark]

The swagger also shows selectionMark as a new field value type. This would fit into our FieldValue and FieldValueType
accordingly:

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
    
In `FormField` we could rename `text` references to `data` or something generic

class FormField:
    label_data: FieldData (was FieldText)
    value_data: FieldData (was FieldText)
    name: str
    confidence: float
    value: typed value (python) or FieldValue

`FieldData` supports our union type or FormContent base type (.NET style heterogeneous list)

class FieldData(FormContent):
    text_content: Union[FormWord, FormLine, SelectionMark] or IReadOnlyList<FormContent>

class FormContent:
    page_number: int
    bounding_box: BoundingBox
    text: str

class SelectionMark(FormContent):
    confidence: float
    state: SelectionMarkState enum = "selected", "unselected"

Another rename we might want to consider is that of `text_content` as this now would return `SelectionMark`... this also
has naming implications for the parameter `include_text_content`.

Link to swagger: https://github.com/Azure/azure-rest-api-specs/blob/8d87a7c7caf59182943b890e7576c04d26642f6f/specification/cognitiveservices/data-plane/FormRecognizer/preview/v2.1-preview.1/FormRecognizer.json