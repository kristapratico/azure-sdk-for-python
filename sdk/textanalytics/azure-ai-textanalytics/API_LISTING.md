
## Design

The Text Analytics SDK provides a single client that allows you to engage with the Azure Text Analytics API.

The client includes analysis of batched documents and is created with an endpoint and credential. 
The credential can be a `TextAnalyticsApiKeyCredential(<"api_key">)` or a token credential from azure.identity.

The batched operations will accept the documents parameter as a `list[str]`, `list[DetectLanguageInput]`, 
`list[TextDocumentInput]`, or dict-like representation of the objects. If the user passes in a `list[str]` the ID 
will be set internally (0 based) and the country_hint/language will use the default. Mixing the two types of inputs 
will be explicitly disallowed. The batched operations will return a response consisting of a combined list of 
the results and errors in the order that the user passed in the documents.


## TextAnalyticsClient
```python
azure.ai.textanalytics.TextAnalyticsClient(endpoint, credential)
```

The client accepts keyword arguments `default_language_hint` and `default_country_hint` to specify the default
hint for all operations.

### Client operations

```python
# Returns list[Union[DetectLanguageResult, DocumentError]]
TextAnalyticsClient.detect_language(documents, country_hint=None, **kwargs)

# Returns list[Union[RecognizeEntitiesResult, DocumentError]]
TextAnalyticsClient.recognize_entities(documents, language=None, **kwargs)

# Returns list[Union[RecognizePiiEntitiesResult, DocumentError]]
TextAnalyticsClient.recognize_pii_entities(documents, language=None, **kwargs)

# Returns list[Union[RecognizeLinkedEntitiesResult, DocumentError]]
TextAnalyticsClient.recognize_linked_entities(documents, language=None, **kwargs)

# Returns list[Union[ExtractKeyPhrasesResult, DocumentError]]
TextAnalyticsClient.extract_key_phrases(documents, language=None, **kwargs)

# Returns list[Union[AnalyzeSentimentResult, DocumentError]]
TextAnalyticsClient.analyze_sentiment(documents, language=None, **kwargs)
```

Keyword arguments `model_version` and `show_stats` can be passed per-operation to specify the model version to use 
for analysis and whether to include document level statistics.


## Scenarios

### 1. Detect language for a batch of documents.
```python
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential=TextAnalyticsApiKeyCredential("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),
)

# documents can be a list[str], list[DetectLanguageInput], or dict-like representation of object
documents = ["This is written in English", "Este es un document escrito en Español."]

documents = [{"id": "1", "country_hint": "US", "text": "This is written in English"}, 
             {"id": "2", "country_hint": "ES", "text": "Este es un document escrito en Español."}]

response = client.detect_language(documents)  # list[Union[DetectLanguageResult, DocumentError]]
result = [doc for doc in response if not doc.is_error]

for doc in result:
    print("Language detected: {}".format(doc.primary_language.name))
    print("ISO6391 name: {}".format(doc.primary_language.iso6391_name))
    print("Confidence score: {}\n".format(doc.primary_language.score))
```

### 2. Recognize entities in a batch of documents.
```python
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential=TextAnalyticsApiKeyCredential("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),
)

documents = ["Satya Nadella is the CEO of Microsoft", "Elon Musk is the CEO of SpaceX and Tesla."]

response = client.recognize_entities(documents)  # list[Union[RecognizeEntitiesResult, DocumentError]]
result = [doc for doc in response if not doc.is_error]

for doc in result:
    for entity in doc.entities:
        print("Entity: {}".format(entity.text))
        print("Category: {}".format(entity.category))
        print("Subcategory: {}".format(entity.subcategory))
        print("Confidence score: {}".format(entity.score))
```

### 3. Recognize personally identifiable information in a batch of documents.
```python
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential=TextAnalyticsApiKeyCredential("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),
)

documents = ["My SSN is 555-55-5555", "Visa card 4147999933330000"]

response = client.recognize_pii_entities(documents)   # list[Union[RecognizePiiEntitiesResult, DocumentError]]
result = [doc for doc in response if not doc.is_error]

for doc in result:
    for entity in doc.entities:
        print("Entity: {}".format(entity.text))
        print("Category: {}".format(entity.category))
        print("Subcategory: {}".format(entity.subcategory))
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

response = client.recognize_linked_entities(documents)  # list[Union[RecognizeLinkedEntitiesResult, DocumentError]]
result = [doc for doc in response if not doc.is_error]

for doc in result:
    for entity in doc.entities:
        print("Entity: {}".format(entity.name))
        print("Url: {}".format(entity.url))
        print("Data Source: {}".format(entity.data_source))
```

### 5. Extract key phrases in a batch of documents.
```python
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential=TextAnalyticsApiKeyCredential("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),
)

documents = ["My cat might need to see a veterinarian", "The pitot tube is used to measure airspeed."]

response = client.extract_key_phrases(documents)  # list[Union[ExtractKeyPhrasesResult, DocumentError]]
result = [doc for doc in response if not doc.is_error]

for doc in result:
    for phrase in doc.key_phrases:
        print(phrase)
```

### 6. Analyze sentiment in a batch of documents.
```python
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential=TextAnalyticsApiKeyCredential("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),
)

documents = ["The hotel was dark and unclean.", "The restaurant had amazing gnocci."]

response = client.analyze_sentiment(documents)   # list[Union[AnalyzeSentimentResult, DocumentError]]
result = [doc for doc in response if not doc.is_error]

for doc in result:
    print("Overall sentiment: {}".format(doc.sentiment))
    print("Overall scores: positive={}; neutral={}; negative={} \n".format(
        doc.sentiment_scores.positive,
        doc.sentiment_scores.neutral,
        doc.sentiment_scores.negative,
    ))
```