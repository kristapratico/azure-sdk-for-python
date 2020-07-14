The training methods in the SDK return a `CustomFormModel`:

```python
class CustomFormModel:
    model_id: str
    status: CustomFormModelStatus
    training_started_on: datetime
    training_completed_on: datetime
    submodels: List[CustomFormSubModel]
    errors = List[FormRecognizerError]
    training_documents = List[TrainingDocumentInfo]
```

This is built and mapped from the swagger type that is returned - `Model`:

```python
class Model:
    model_info: ModelInfo       # (where model_id, status, training_started_on, training_completed_on come from)
    keys: KeysResult            # (where submodels comes from if unsupervised)
    train_result: TrainResult   # (where submodels, errors, and training_documents come from)
    composed_train_results: Dict[str, TrainResult]  # (this is added in 2.1)
```

Design after syncing with Anne:

`CustomFormModel` does not change - we just re-adjust mapping for a composed model.

```python
class CustomFormModel:
    model_id: str
    status: CustomFormModelStatus
    training_started_on: datetime
    training_completed_on: datetime
    submodels: List[CustomFormSubModel]
    errors: List[FormRecognizerError]               # union of all errors from submodels, or just don't return for composed model
    training_documents: List[TrainingDocumentInfo]  # union of all training documents from submodels, or just don't return for composed model
```

`model_id` property is added to `CustomFormSubmodel` to help associate the submodel with the original model
in a composed model, otherwise is None/null.

```python
class CustomFormSubmodel:
    model_id: str
    accuracy: float
    fields: Dict[str, CustomFormModelField]
    form_type: str

class CustomFormModelField:
    label: str
    name: str
    accuracy: float
```

-----------------------------------------------------------------------------------------------------------------------

To get the new composed train result to fit into our existing design, I think we have two reasonable choices:

1) Add a `composed_train_results` property to the `CustomFormModel`, and set the `submodels`, `errors`, and `training_documents`
properties to None/null if a composed model is returned. Create a new model called `ComposedTrainResult` which will consist of these
3 properties and return a `composed_train_results: Dict[str, ComposedTrainResult]` on `CustomFormModel`:

```python
class CustomFormModel:
    model_id: str
    status: str
    training_started_on: datetime
    training_completed_on: datetime
    submodels: List[CustomFormSubModel]  # None if a composed model
    errors: List[FormRecognizerError]  # None if a composed model
    training_documents: List[TrainingDocumentInfo]  # None if a composed model
    composed_train_result: Dict[str, ComposedTrainResult]  # None if not a composed model
```

This favors the non-composed model scenario which is probably more commonly used. And has no breaking change this preview.

2) Create a new model called `TrainResult` which consists of `submodels`, `errors`, and 
`training_documents` and remove these top-level properties from `CustomFormModel`:

```python
class CustomFormModel:
    model_id: str
    status: str
    training_started_on: datetime
    training_completed_on: datetime
    train_result: TrainResult  # None if a composed model
    composed_train_result: Dict[str, TrainResult]  # None if not a composed model


class TrainResult:
    submodels: List[CustomFormSubModel]
    errors = List[FormRecognizerError]
    training_documents = List[TrainingDocumentInfo]
```

This aligns more with the swagger type, and doesn't necessarily favor a "normal" model over a composed one. It _might_
clear up some confusion since there wouldn't be many None/null properties at the top-level for the composed model.
However, this would make the fields and errors harder to reach in all scenarios and require a breaking change during 
preview 5 before we GA.
