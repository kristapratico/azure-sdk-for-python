# Azure Text Analytics Python SDK

## Design

The Text Analytics SDK provides a single client that allows you to engage with the Azure Text Analytics API.

The client includes analysis of batched documents and single text operations for new users getting started with 
text analytics. The client is created with an endpoint and credential. 
The credential string is the user's cognitive services key.

The batched operations will accept the documents parameter as a `list[str]` or `list[(Multi)LanguageInput]`. 
If the user passes in a `list[str]` the ID will be set internally (0 based) and the country_hint/language 
will use the default. Mixing the two types of inputs will be explicitly disallowed. The batched operations will
return a response consisting of a combined list of the results and errors in the order that the user passed in
the documents.

The module level, single text operations do not get assigned an ID and move the request statistics and 
model_version results to a response hook. The user can pass in a country_hint or language hint as an optional 
parameter. If the operation fails, the exception is raised with an error message.

## TextAnalyticsClient
```python
azure.cognitiveservices.language.textanalytics.TextAnalyticsClient(endpoint, credential)
```
### Client operations

```python
# Returns list[Union[DocumentLanguage, DocumentError]]
TextAnalyticsClient.detect_language(documents, model_version=None, show_stats=False, country_hint=None, **kwargs)

# Returns list[Union[DocumentEntities, DocumentError]]
TextAnalyticsClient.recognize_entities(documents, model_version=None, show_stats=False, language=None, **kwargs)

# Returns list[Union[DocumentEntities, DocumentError]]
TextAnalyticsClient.recoognize_pii_entities(documents, model_version=None, show_stats=False, language=None, **kwargs)

# Returns list[Union[DocumentLinkedEntities, DocumentError]]
TextAnalyticsClient.recognize_linked_entities(documents, model_version=None, show_stats=False, language=None, **kwargs)

# Returns list[Union[DocumentKeyPhrases, DocumentError]]
TextAnalyticsClient.extract_key_phrases(documents, model_version=None, show_stats=False, language=None, **kwargs)

# Returns list[Union[DocumentSentiment, DocumentError]]
TextAnalyticsClient.analyze_sentiment(documents, model_version=None, show_stats=False, language=None, **kwargs)
```

### Module level operations

```python
from azure.cognitiveservices.language.textanalytics import (
    single_detect_language,
    single_recognize_entities,
    single_recognize_pii_entities,
    single_recognize_linked_entities,
    single_extract_key_phrases,
    single_analyze_sentiment,
)

# Returns DocumentLanguage
single_detect_language(
    endpoint, credential, text, country_hint=None, model_version=None, show_stats=False, **kwargs)

# Returns DocumentEntities
single_recognize_entities(
    endpoint, credential, text, language=None, model_version=None, show_stats=False, **kwargs)

# Returns DocumentEntities
single_recognize_pii_entities(
    endpoint, credential, text, language=None, model_version=None, show_stats=False, **kwargs)

# Returns DocumentLinkedEntities
single_recognize_linked_entities(
    endpoint, credential, text, language=None, model_version=None, show_stats=False, **kwargs)

# Returns DocumentKeyPhrases
single_extract_key_phrases(
    endpoint, credential, text, language=None, model_version=None, show_stats=False, **kwargs)

# Returns DocumentSentiment
single_analyze_sentiment(
    endpoint, credential, text, language=None, model_version=None, show_stats=False, **kwargs)
```

## Scenarios

### Client Operations

### 1. Detect language for a batch of documents.
```python
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
)

# documents can be a list[str] or list[LanguageInput]
documents = ["This is written in English", "Este es un document escrito en Español."]

documents = [{"id": "1", "country_hint": "US", "text": "This is written in English"}, 
             {"id": "2", "country_hint": "es", "text": "Este es un document escrito en Español."}]

# request statistics, model_version go to response hook
response = client.detect_language(documents=documents)  # list[Union[DocumentLanguage, DocumentError]]

docs = [doc for doc in response if not doc.is_error]

for doc in docs:
    print(doc.detected_language.name)
    print(doc.detected_language.iso6391_name)
    print(doc.detected_language.score)
```

### 2. Recognize entities in a batch of documents.
```python
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
)

# documents can be a list[str] or list[MultiLanguageInput]
documents = ["Satya Nadella is the CEO of Microsoft", "Elon Musk is the CEO of SpaceX and Tesla."]

response = client.recognize_entities(documents=documents)  # list[Union[DocumentEntities, DocumentError]]

docs = [doc for doc in response if not doc.is_error]

for doc in docs:
    for entity in doc.entities:
        print(entity.text)
        print(entity.type)
        print(entity.sub_type)
        print(entity.score)
```

### 3. Recognize personally identifiable information in a batch of documents.
```python
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
)

# documents can be a list[str] or list[MultiLanguageInput]
documents = ["My SSN is 555-55-5555", "Visa card 4147999933330000"]

response = client.recognize_pii_entities(documents=documents)   # list[Union[DocumentEntities, DocumentError]]

docs = [doc for doc in response if not doc.is_error]

for doc in docs:
    for entity in doc.entities:
        print(entity.text)
        print(entity.type)
        print(entity.sub_type)
        print(entity.score)
```

### 4. Recognize linked entities in a batch of documents.
```python
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
)

# documents can be a list[str] or list[MultiLanguageInput]
documents = ["Old Faithful is a geyser at Yellowstone Park", "Mount Shasta has lenticular clouds."]

response = client.recognize_linked_entities(documents=documents)  # list[Union[DocumentLinkedEntities, DocumentError]]

docs = [doc for doc in response if not doc.is_error]

for doc in docs:
    for entity in doc.entities:
        print(entity.name)
        print(entity.url)
        print(entity.data_source)
```

### 5. Extract key phrases in a batch of documents.
```python
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
)

# documents can be a list[str] or list[MultiLanguageInput]
documents = ["My cat might need to see a veterinarian", "The pitot tube is used to measure airspeed."]

response = client.extract_key_phrases(documents=documents)  # list[Union[DocumentKeyPhrases, DocumentError]]

docs = [doc for doc in response if not doc.is_error]

for doc in docs:
    for phrase in doc.key_phrases:
        print(phrase)
```

### 6. Analyze sentiment in a batch of documents.
```python
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
)

# documents can be a list[str] or list[MultiLanguageInput]
documents = ["The hotel was dark and unclean.", "The restaurant had amazing gnocci."]

response = client.analyze_sentiment(documents=documents)   # list[Union[DocumentSentiment, DocumentError]]

docs = [doc for doc in response if not doc.is_error]

for doc in docs:
    print(doc.sentiment)
    print(doc.document_scores)
```

### Module Level Operations

### 7. Detect language in text.
```python
from azure.cognitiveservices.language.textanalytics import single_detect_language

response = single_detect_language(  
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
    text="This is written in English",
) # DocumentLanguage

print(response.detected_language.name)
print(response.detected_language.iso6391_name)
print(response.detected_language.score)
```

### 8. Recognize entities in text.
```python
from azure.cognitiveservices.language.textanalytics import single_recognize_entities

response = single_recognize_entities(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
    text="Satya Nadella is the CEO of Microsoft",
) # DocumentEntities

for entity in response.entities:
    print(entity.text)
    print(entity.type)
    print(entity.sub_type)
    print(entity.score)
```

### 9. Recognize personally identifiable information in text.
```python
from azure.cognitiveservices.language.textanalytics import single_recognize_pii_entities

response = single_recognize_pii_entities(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
    text="My SSN is 555-55-5555",
) # DocumentEntities

for entity in response.entities:
    print(entity.text)
    print(entity.type)
    print(entity.sub_type)
    print(entity.score)
```

### 10. Recognize linked entities in text.
```python
from azure.cognitiveservices.language.textanalytics import single_recognize_linked_entities

response = single_recognize_linked_entities(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
    text="Old Faithful is a geyser at Yellowstone Park",
) # DocumentLinkedEntities

for entity in response.entities:
    print(entity.name)
    print(entity.url)
    print(entity.data_source)
```

### 11. Recognize key phrases in text.
```python
from azure.cognitiveservices.language.textanalytics import single_extract_key_phrases

response = single_extract_key_phrases( 
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
    text="My cat might need to see a veterinarian",
) # DocumentKeyPhrases

print(response.key_phrases)
```

### 12. Analyze sentiment in text.
```python
from azure.cognitiveservices.language.textanalytics import single_analyze_sentiment

response = single_analyze_sentiment(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
    text="I will never fly Spirit airlines again."
) # DocumentSentiment

print(response.sentiment)
print(response.document_scores)
```