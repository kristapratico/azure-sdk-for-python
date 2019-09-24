# Azure Text Analytics Python SDK

## Design

The Text Analytics SDK provides a single client that allows you to engage with the Azure Text Analytics API.

The client includes analysis of batched documents and single text operations for new users getting started with 
text analytics. The client is created with an endpoint and credential. 
The credential string is the user's cognitive services key.

The batched operations will accept the documents parameter as a `list[str]` or `list[(Multi)LanguageInput]`. 
If the user passes in a `list[str]` the ID will be set internally (0 based) and the country_hint/language 
will use the default. Mixing the two types of inputs will be explicitly disallowed.

The module level, single text operations do not get assigned an ID and move the statistics and model_version results 
to a response hook. The user can pass in a country_hint or language hint as an optional parameter. 
If the operation fails, the exception is raised with an error message.

## TextAnalyticsClient
```python
azure.cognitiveservices.language.textanalytics.TextAnalyticsClient(endpoint, credential)
```
### Client operations

```python
# Returns list[Union(DocumentLanguage, DocumentError)]
TextAnalyticsClient.detect_language(documents, model_version=None, show_stats=False, **kwargs)

# Returns list[Union(DocumentEntities, DocumentError)]
TextAnalyticsClient.detect_entities(documents, model_version=None, show_stats=False, **kwargs)

# Returns list[Union(DocumentHealthcareEntities, DocumentError)]
TextAnalyticsClient.detect_healthcare_entities(documents, model_version=None, show_stats=False, **kwargs)

# Returns list[Union(DocumentEntities, DocumentError)]
TextAnalyticsClient.detect_pii_entities(documents, model_version=None, show_stats=False, **kwargs)

# Returns list[Union(DocumentLinkedEntities, DocumentError)]
TextAnalyticsClient.detect_linked_entities(documents, model_version=None, show_stats=False, **kwargs)

# Returns list[Union(DocumentKeyPhrases, DocumentError)]
TextAnalyticsClient.detect_key_phrases(documents, model_version=None, show_stats=False, **kwargs)

# Returns list[Union(DocumentSentiment, DocumentError)]
TextAnalyticsClient.detect_sentiment(documents, model_version=None, show_stats=False, **kwargs)
```

### Module level operations

```python
from azure.cognitiveservices.language.textanalytics import (
    single_detect_language,
    single_detect_entities,
    single_detect_healthcare_entities,
    single_detect_pii_entities,
    single_detect_linked_entities,
    single_detect_key_phrases,
    single_detect_sentiment,
)

# Returns list[DetectedLanguage]
single_detect_language(
    endpoint, credential, text, country_hint="US", model_version=None, show_stats=False, **kwargs)

# Returns list[Entity]
single_detect_entities(
    endpoint, credential, text, language="en", model_version=None, show_stats=False, **kwargs)

# Returns list[DocumentHealthcareEntities]
single_detect_healthcare_entities(
    endpoint, credential, text, language="en", model_version=None, show_stats=False, **kwargs)

# Returns list[Entity]
single_detect_pii_entities(
    endpoint, credential, text, language="en", model_version=None, show_stats=False, **kwargs)

# Returns list[LinkedEntity]
single_detect_linked_entities(
    endpoint, credential, text, language="en", model_version=None, show_stats=False, **kwargs)

# Returns list[str]
single_detect_key_phrases(
    endpoint, credential, text, language="en", model_version=None, show_stats=False, **kwargs)

# Returns DocumentSentiment
single_detect_sentiment(
    endpoint, credential, text, language="en", model_version=None, show_stats=False, **kwargs)
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
response = client.detect_language(documents=documents)  # list[Union(DocumentLanguage, DocumentError)]

docs = [doc for doc in response if not doc.is_error]

for doc in docs:
    for language in doc.detected_language:
        print(language.name)
        print(language.iso6391_name)
        print(language.score)
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

response = client.detect_entities(documents=documents)  # list[Union(DocumentEntities, DocumentError)]

docs = [doc for doc in response if not doc.is_error]

for doc in docs:
    for entity in doc.entities:
        print(entity.text)
        print(entity.type)
        print(entity.sub_type)
        print(entity.score)
        print(entity.offset)
        print(entity.length)
```

### 3. Recognize healthcare entities in a batch of documents.
```python
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
)

# documents can be a list[str] or list[MultiLanguageInput]
documents = ["Patient should take 40mg ibuprofen twice a week.", 
             "Patient has a fever and sinus infection."]

response = client.detect_healthcare_entities(documents=documents)  # list[Union(DocumentHealthcareEntities, DocumentError)]

docs = [doc for doc in response if not doc.is_error]

for doc in docs:
    for entity in doc.entities:
        print(entity.id)
        print(entity.type)
        print(entity.category)
        print(entity.score)
        print(entity.offset)
        print(entity.umls_id)
    for relation in doc.relations:
        print(relation.relation_type)
        print(relation.score)
```

### 4. Recognize personally identifiable information in a batch of documents.
```python
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
)

# documents can be a list[str] or list[MultiLanguageInput]
documents = ["My SSN is 555-55-5555", "Visa card 4147999933330000"]

response = client.batch_detect_pii_entities(documents=documents)   # list[Union(DocumentEntities, DocumentError)]

docs = [doc for doc in response if not doc.is_error]

for doc in docs:
    for entity in doc.entities:
        print(entity.text)
        print(entity.type)
        print(entity.sub_type)
        print(entity.score)
        print(entity.offset)
        print(entity.length)
```

### 5. Recognize linked entities in a batch of documents.
```python
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
)

# documents can be a list[str] or list[MultiLanguageInput]
documents = ["Old Faithful is a geyser at Yellowstone Park", "Mount Shasta has lenticular clouds."]

response = client.detect_linked_entities(documents=documents)  # list[Union(DocumentLinkedEntities, DocumentError)]

docs = [doc for doc in response if not doc.is_error]

for doc in docs:
    for entity in doc.entities:
        print(entity.name)
        print(entity.url)
        print(entity.data_source)
```

### 6. Recognize key phrases in a batch of documents.
```python
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
)

# documents can be a list[str] or list[MultiLanguageInput]
documents = ["My cat might need to see a veterinarian", "The pitot tube is used to measure airspeed."]

response = client.detect_key_phrases(documents=documents)  # list[Union(DocumentKeyPhrases, DocumentError)]

docs = [doc for doc in response if not doc.is_error]

for doc in docs:
    print(doc.key_phrases)
```

### 7. Detect sentiment in a batch of documents.
```python
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
)

# documents can be a list[str] or list[MultiLanguageInput]
documents = ["The hotel was dark and unclean.", "The restaurant had amazing gnocci."]

response = client.detect_sentiment(documents=documents)   # list[Union(DocumentSentiment, DocumentError)]

docs = [doc for doc in response if not doc.is_error]

for doc in docs:
    print("Sentiment: ", doc.sentiment)
    print("Score: ", doc.document_scores)
```

### Module Level Operations

### 8. Detect language in text.
```python
from azure.cognitiveservices.language.textanalytics import single_detect_language

response = single_detect_language(  
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
    text="This is written in English",
) # list[DetectedLanguage]

print(response[0].name)
print(response[0].iso6391_name)
print(response[0].score)
```

### 9. Recognize entities in text.
```python
from azure.cognitiveservices.language.textanalytics import single_detect_entities

response = single_detect_entities(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
    text="Satya Nadella is the CEO of Microsoft",
) # list[Entity]

for entity in response:
    print(entity.text)
    print(entity.type)
    print(entity.sub_type)
    print(entity.score)
    print(entity.offset)
    print(entity.length)
```

### 10. Recognize healthcare entities in text.
```python
from azure.cognitiveservices.language.textanalytics import single_detect_healthcare_entities

response = single_detect_healthcare_entities(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
    text="Patient manages his diabetes with insulin"
) # list[DocumentHealthcareEntities]

for entity in response.entities:
    print(entity.id)
    print(entity.type)
    print(entity.category)
    print(entity.score)
    print(entity.offset)
    print(entity.umls_id)
for relation in response.relations:
    print(relation.relation_type)
    print(relation.score)
```

### 11. Recognize personally identifiable information in text.
```python
from azure.cognitiveservices.language.textanalytics import single_detect_pii_entities

response = single_detect_pii_entities(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
    text="My SSN is 555-55-5555",
) # list[Entity]

for entity in response:
    print(entity.text)
    print(entity.type)
    print(entity.sub_type)
    print(entity.score)
    print(entity.offset)
    print(entity.length)
```

### 12. Recognize linked entities in text.
```python
from azure.cognitiveservices.language.textanalytics import single_detect_linked_entities

response = single_detect_linked_entities(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
    text="Old Faithful is a geyser at Yellowstone Park",
) # list[LinkedEntity]

for entity in response:
    print(entity.name)
    print(entity.url)
    print(entity.data_source)
```

### 13. Recognize key phrases in text.
```python
from azure.cognitiveservices.language.textanalytics import single_detect_key_phrases

response = single_detect_key_phrases( 
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
    text="My cat might need to see a veterinarian",
) # list[str]

print(response)
```

### 14. Detect sentiment in text.
```python
from azure.cognitiveservices.language.textanalytics import single_detect_sentiment

response = single_detect_sentiment(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
    text="I will never fly Spirit airlines again."
) # DocumentSentiment

print("Sentiment: ", response.sentiment)
print("Score: ", response.document_scores)
```