# Azure Text Analytics Python SDK

## Design

The Text Analytics SDK provides a single client that allows you to engage with the Azure Text Analytics API.

The client includes text analysis of batched documents and single text operations.
The client is created with an endpoint and credential. The credential string is the user's cognitive services key.

The batched operations will accept the documents parameter as a `list[str]` or `list[(Multi)LanguageInput]`. If the user
passes in a `list[str]` the ID will be added behind the scenes (0 based) and the country_hint/language will use the 
default. A mix of `list[str]` and `list[(Multi)LanguageInput]` is disallowed.

The single text operations do not get assigned an ID and move the statistics and model_version results to a 
response hook. The user can pass in a country_hint or language hint as an optional parameter. If the operation fails, 
the exception is raised with an error message.

## TextAnalyticsClient

```python
azure.cognitiveservices.language.textanalytics.TextAnalyticsClient(endpoint, credential)

# Text Analytics operations

# Returns LanguageResult
TextAnalyticsClient.batch_detect_language(documents, model_version=None, show_stats=False, **kwargs)

# Returns list[DetectedLanguage]
TextAnalyticsClient.detect_language(text, country_hint="US", model_version=None, show_stats=False, **kwargs)

# Returns EntitiesResult
TextAnalyticsClient.batch_detect_entities(documents, model_version=None, show_stats=False, **kwargs)

# Returns list[Entity]
TextAnalyticsClient.detect_entities(text, language="en", model_version=None, show_stats=False, **kwargs)

# Returns HealthcareResult
TextAnalyticsClient.batch_detect_healthcare_entities(documents, model_version=None, show_stats=False, **kwargs)

# Returns list[DocumentHealthcareEntities]
TextAnalyticsClient.detect_healthcare_entities(text, language="en", model_version=None, show_stats=False, **kwargs)

# Returns EntitiesResult
TextAnalyticsClient.batch_detect_pii_entities(documents, model_version=None, show_stats=False, **kwargs)

# Returns list[Entity]
TextAnalyticsClient.detect_pii_entities(text, language="en", model_version=None, show_stats=False, **kwargs)

# Returns EntityLinkingResult
TextAnalyticsClient.batch_detect_linked_entities(documents, model_version=None, show_stats=False, **kwargs)

# Returns list[LinkedEntity]
TextAnalyticsClient.detect_linked_entities(text, language="en", model_version=None, show_stats=False, **kwargs)

# Returns KeyPhraseResult
TextAnalyticsClient.batch_detect_key_phrases(documents, model_version=None, show_stats=False, **kwargs)

# Returns list[str]
TextAnalyticsClient.detect_key_phrases(text, language="en", model_version=None, show_stats=False, **kwargs)

# Returns SentimentResponse
TextAnalyticsClient.batch_detect_sentiment(documents, model_version=None, show_stats=False, **kwargs)

# Returns DocumentSentiment
TextAnalyticsClient.detect_sentiment(text, language="en", model_version=None, show_stats=False, **kwargs)
```

## Scenarios

### 1. Detect language for a batch of documents.
```python
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
)

# documents can be a list[str] or list[LanguageInput]
docs = ["This is written in English", "Este es un document escrito en Español."]
docs = [{"id": "1", "country_hint": "US", "text": "This is written in English"}, 
        {"id": "2", "country_hint": "es", "text": "Este es un document escrito en Español."}]


response = client.batch_detect_language(documents=docs)  # LanguageResult

for doc in response.documents:
    print(doc.id)
    print(doc.statistics)
    for language in doc.detected_languages:
        print(language.name)
        print(language.iso6391_name)
        print(language.score)
```

### 2. Detect language in text.
```python
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
)

response = client.detect_language("This is written in English")  # list[DetectedLanguage]

print(response[0].name)
print(response[0].iso6391_name)
print(response[0].score)
```

### 3. Recognize entities in a batch of documents.
```python
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
)

# documents can be a list[str] or list[MultiLanguageInput]
docs = ["Satya Nadella is the CEO of Microsoft", "Elon Musk is the CEO of SpaceX and Tesla."]

response = client.batch_detect_entities(documents=docs)  # EntitiesResult

for text in response.documents:
    print(text.id)
    print(text.statistics)
    for entity in text.entities:
        print(entity.text)
        print(entity.type)
        print(entity.sub_type)
        print(entity.score)
        print(entity.offset)
        print(entity.length)
```

### 4. Recognize entities in text.
```python
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
)

response = client.detect_entities("Satya Nadella is the CEO of Microsoft")  # list[Entity]

for entity in response:
    print(entity.text)
    print(entity.type)
    print(entity.sub_type)
    print(entity.score)
    print(entity.offset)
    print(entity.length)
```

### 5. Recognize healthcare entities in a batch of documents.
```python
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
)

# documents can be a list[str] or list[MultiLanguageInput]
docs = ["Patient should take 40mg ibuprofen twice a week.", 
        "Patient has a fever and sinus infection."]

response = client.batch_detect_healthcare_entities(documents=docs)  # HealthcareResult

for text in response.documents:
    print(text.id)
    print(text.statistics)
    for entity in text.entities:
        print(entity.id)
        print(entity.type)
        print(entity.category)
        print(entity.score)
        print(entity.offset)
        print(entity.umls_id)
    for relation in text.relations:
        print(relation.relation_type)
        print(relation.score)
```

### 6. Recognize healthcare entities in text.
```python
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
)

response = client.detect_healthcare_entities("Patient manages his diabetes with insulin")  # list[DocumentHealthcareEntities]

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

### 7. Recognize personally identifiable information in a batch of documents.
```python
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
)

# documents can be a list[str] or list[MultiLanguageInput]
docs = ["My SSN is 555-55-5555", "Visa card 4147999933330000"]

response = client.batch_detect_pii_entities(documents=docs)  # EntitiesResult

for text in response.documents:
    print(text.id)
    print(text.statistics)
    for entity in text.entities:
        print(entity.text)
        print(entity.type)
        print(entity.sub_type)
        print(entity.score)
        print(entity.offset)
        print(entity.length)
```

### 8. Recognize personally identifiable information in text.
```python
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
)

response = client.detect_pii_entities("My SSN is 555-55-5555")  # list[Entity]

for entity in response:
    print(entity.text)
    print(entity.type)
    print(entity.sub_type)
    print(entity.score)
    print(entity.offset)
    print(entity.length)
```

### 9. Recognize linked entities in a batch of documents.
```python
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
)

# documents can be a list[str] or list[MultiLanguageInput]
docs = ["Old Faithful is a geyser at Yellowstone Park", "Mount Shasta has lenticular clouds."]

response = client.batch_detect_linked_entities(documents=docs)  # EntityLinkingResult

for text in response.documents:
    print(text.id)
    print(text.statistics)
    for entity in text.entities:
        print(entity.name)
        print(entity.url)
        print(entity.data_source)
```

### 10. Recognize linked entities in text.
```python
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
)

response = client.detect_linked_entities("Old Faithful is a geyser at Yellowstone Park")  # list[LinkedEntity]

for entity in response:
    print(entity.name)
    print(entity.url)
    print(entity.data_source)
```

### 11. Recognize key phrases in a batch of documents.
```python
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
)

# documents can be a list[str] or list[MultiLanguageInput]
docs = ["My cat might need to see a veterinarian", "The pitot tube is used to measure airspeed."]

response = client.batch_detect_key_phrases(documents=docs)  # KeyPhraseResult

for phrases in response.documents:
    print(phrases.key_phrases)
```

### 12. Recognize key phrases in text.
```python
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
)

response = client.detect_key_phrases("My cat might need to see a veterinarian")  # list[str]

print(response)
```

### 13. Detect sentiment in a batch of documents.
```python
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
)

# documents can be a list[str] or list[MultiLanguageInput]
docs = ["The hotel was dark and unclean.", "The restaurant had amazing gnocci."]

response = client.batch_detect_sentiment(documents=docs)  # SentimentResponse

for doc in response.documents:
    print("Sentiment: ", doc.sentiment)
    print("Score: ", doc.document_scores)
```

### 14. Detect sentiment in text.
```python
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient

client = TextAnalyticsClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # cognitive services key
)

response = client.detect_sentiment("I will never fly Spirit airlines again.")  # DocumentSentiment

print("Sentiment: ", response.sentiment)
print("Score: ", response.document_scores)
```