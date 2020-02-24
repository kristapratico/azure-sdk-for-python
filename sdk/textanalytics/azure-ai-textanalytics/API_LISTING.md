
## Text Analytics Design Overview

The Text Analytics SDK provides a single client that allows you to engage with the Azure Text Analytics API.

The client includes analysis of batched documents and is created with an endpoint and credential. 
The credential can be a `TextAnalyticsApiKeyCredential(<"api_key">)` or a token credential from azure.identity.

The batched operations will accept as input a `list[str]`, `list[DetectLanguageInput]`, 
`list[TextDocumentInput]`, or dict-like representation of the objects. If the user passes in a `list[str]` the ID 
will be set internally (0 based) and the country_hint/language will use the default. Mixing the two types of inputs 
will be explicitly disallowed. The batched operations will return a response consisting of a heterogeneous list of 
result and error objects in the order that the user passed in the documents.


## TextAnalyticsClient
```python
azure.ai.textanalytics.TextAnalyticsClient(endpoint, credential)
```

The client accepts keyword arguments `default_language` and `default_country_hint` to specify the default
hint for all operations.

### Client operations

```python
# Returns list[Union[DetectLanguageResult, DocumentError]]
TextAnalyticsClient.detect_language(inputs, **kwargs)

# Returns list[Union[RecognizeEntitiesResult, DocumentError]]
TextAnalyticsClient.recognize_entities(inputs, **kwargs)

# Returns list[Union[RecognizePiiEntitiesResult, DocumentError]]
TextAnalyticsClient.recognize_pii_entities(inputs, **kwargs)

# Returns list[Union[RecognizeLinkedEntitiesResult, DocumentError]]
TextAnalyticsClient.recognize_linked_entities(inputs, **kwargs)

# Returns list[Union[ExtractKeyPhrasesResult, DocumentError]]
TextAnalyticsClient.extract_key_phrases(inputs, **kwargs)

# Returns list[Union[AnalyzeSentimentResult, DocumentError]]
TextAnalyticsClient.analyze_sentiment(inputs, **kwargs)
```

Per-operation keyword arguments:

* `model_version` - specifies the model version to use for analysis
* `show_stats` - indicates whether to return document/request statistics with the response
* `country_hint` - passed into `detect_language` to use a country hint for language detection
* `language` - passed into all other methods to indicate the language of the input documents

## Scenarios

### 1. Analyze sentiment in a batch of documents.
```python
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential=TextAnalyticsApiKeyCredential("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),
)

# documents can be a list[str], dict, list[TextDocumentInput]

documents = [
    {"id": "1", "language": "en", "text": "The hotel was dark and unclean. I wouldn't recommend staying there."}, 
    {"id": "2", "language": "en", "text": "The restaurant had amazing gnocchi! The waiters were excellent."}
]

documents = [
    TextDocumentInput(id="1", language="en", text="The hotel was dark and unclean. I wouldn't recommend staying there."),
    TextDocumentInput(id="2", language="en", text="The restaurant had amazing gnocchi! The waiters were excellent.")
]

documents = [
    "The hotel was dark and unclean. I wouldn't recommend staying there.", 
    "The restaurant had amazing gnocchi! The waiters were excellent."
]

def callback(response):
    print("Model version: {}".format(response.model_version))
    print("Request/Batch statistics:")
    print(response.statistics.document_count)
    print(response.statistics.valid_document_count)
    print(response.statistics.erroneous_document_count)
    print(response.statistics.transaction_count)


result = client.analyze_sentiment(
    documents,
    show_stats=True,
    model_version="latest",
    response_hook=callback
)   # list[Union[AnalyzeSentimentResult, DocumentError]]


for doc in result:
    if doc.is_error:
        print("Cannot analyze sentiment. Document id {}: {}".format(doc.id, doc.error.message))
        continue

    print("Document statistics:")
    print("Number chars: {}".format(doc.statistics.character_count))
    print("Number transactions: {}".format(doc.statistics.transaction_count))

    print("Document sentiment: {}".format(doc.sentiment))
    print("Document confidence scores: positive={}; neutral={}; negative={} \n".format(
        doc.confidence_scores.positive,
        doc.confidence_scores.neutral,
        doc.confidence_scores.negative,
    ))
    for sentence in doc.sentences:
        print("Sentence sentiment: {}".format(sentence.sentiment))
        print("Sentence confidence scores: positive={}; neutral={}; negative={}; \
                length of sentence: {}; offset: {}".format(
            sentence.confidence_scores.positive,
            sentence.confidence_scores.neutral,
            sentence.confidence_scores.negative,
            sentence.length,
            sentence.offset
        ))
```

### 2. Detect language for a batch of documents.
```python
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential=TextAnalyticsApiKeyCredential("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),
)

# documents can be a list[str], dict, list[DetectLanguageInput]
documents = [{"id": "1", "country_hint": "US", "text": "This is written in English"}, 
             {"id": "2", "country_hint": "ES", "text": "Este es un document escrito en Español."}]


response = client.detect_language(documents)  # list[Union[DetectLanguageResult, DocumentError]]
result = [doc for doc in response if not doc.is_error]

for doc in result:
    print("Language detected: {}".format(doc.primary_language.name))
    print("ISO6391 name: {}".format(doc.primary_language.iso6391_name))
    print("Confidence score: {}\n".format(doc.primary_language.score))
```

### 3. Recognize entities in a batch of documents.
```python
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential=TextAnalyticsApiKeyCredential("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),
)

documents = ["Satya Nadella is the CEO of Microsoft", "Elon Musk is the CEO of SpaceX and Tesla."]

result = client.recognize_entities(documents, language="en")  # list[Union[RecognizeEntitiesResult, DocumentError]]
doc_errors = []

for doc in result:
    if doc.is_error:
        doc_errors.append(doc.id, doc.error.message)
        continue
    for entity in doc.entities:
        print("Entity: {}".format(entity.text))
        print("Category: {}".format(entity.category))
        print("Subcategory: {}".format(entity.subcategory))
        print("Entity length: {}".format(entity.length))
        print("Entity offset: {}".format(entity.offset))
        print("Confidence score: {}".format(entity.score))
```

### 4. Recognize linked entities in a batch of documents.
```python
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential=TextAnalyticsApiKeyCredential("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),
)

documents = ["Old Faithful is a geyser at Yellowstone Park", "Mount Shasta has lenticular clouds."]

response = client.recognize_linked_entities(
    documents,
    language="en"
)  # list[Union[RecognizeLinkedEntitiesResult, DocumentError]]

result = [doc for doc in response if not doc.is_error]

for doc in result:
    for entity in doc.entities:
        print("Entity: {}".format(entity.name))
        print("Url: {}".format(entity.url))
        print("Data source: {}".format(entity.data_source))
        print("Data source entity ID: {}".format(entity.data_source_entity_id))
        for match in entity.matches:
            print("Entity in text: {}\n".format(match.text))
            print("Score: {}".format(match.score))
            print("Offset: {}".format(match.offset))
            print("Length: {}\n".format(match.length))
```

### 5. Recognize personally identifiable information in a batch of documents.
```python
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential=TextAnalyticsApiKeyCredential("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),
)

documents = ["My SSN is 555-55-5555", "Visa card 4111 1111 1111 1111"]

response = client.recognize_pii_entities(
    documents,
    language="en"
)  # list[Union[RecognizePiiEntitiesResult, DocumentError]]

result = [doc for doc in response if not doc.is_error]

for doc in result:
    for entity in doc.entities:
        print("Entity: {}".format(entity.text))
        print("Category: {}".format(entity.category))
        print("Subcategory: {}".format(entity.subcategory))
        print("Entity length: {}".format(entity.length))
        print("Entity offset: {}".format(entity.offset))
        print("Confidence score: {}".format(entity.score))
```

### 6. Extract key phrases in a batch of documents.
```python
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential=TextAnalyticsApiKeyCredential("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),
)

documents = [
    "The food was delicious and there were wonderful staff.", 
    "The pitot tube is used to measure airspeed."
]

response = client.extract_key_phrases(documents, language="en")  # list[Union[ExtractKeyPhrasesResult, DocumentError]]
result = [doc for doc in response if not doc.is_error]

for doc in result:
    for phrase in doc.key_phrases:
        print(phrase)
```
