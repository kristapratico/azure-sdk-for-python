# Static Type Checking Cheat Sheet

This cheat sheet details guidance for typing as it relates to the Python SDK. It should be used with your own judgment to achieve the best balance of clarity and flexibility for your Python client library. 


DO provide type hints (per PEP 484) to public APIs in the client library.
DO NOT use comment style type hints. Use inline, annotation style.
  
```python
# No:
def create_table(table_name):
    # type: (str) -> Table
    ...

# Yes:
def create_table(table_name: str) -> Table:
    ...
```

DO fully annotate function signatures - this includes type annotations for all parameters and the return type.
YOU SHOULD type annotate variables if the type in the code is different from expected or provides more value than what is already provided by Python itself.

```python
# No:
table_name: str = "mytable"  # I can tell it's a string, not necessary
create_table(table_name)

# Yes:
table_map: dict[str, Table] = {}  # clarifies what the dictionary expects
table_map[table_name] = create_table(table_name)
```

DO use mypy and pyright type checkers to statically type check your client library code.
DO add type hints directly to the source code - stub files should not be necessary unless used for third-party libraries or extension modules.
DO mark your client library package to distribute type hints according to [PEP 561](https://peps.python.org/pep-0561/).
DO use the latest typing features available. If not supported by older versions of Python, consider taking a dependency and importing from `typing-extensions`.

```python
# from typing import TypedDict Python >3.8
from typing_extensions import TypedDict
```

DO NOT import types from `typing` or `typing-extensions` under a `typing.TYPE_CHECKING` block. You can import other types under TYPE_CHECKING to avoid a circular import or import a type which is only needed in type annotations and is otherwise costly to load at runtime.

```python
from typing import TYPE_CHECKING

# No:
if TYPE_CHECKING:
    from typing import Union, TypeVar, Any


# Yes:
if TYPE_CHECKING:
    from a import b  # avoiding a circular import
    from c import ExpensiveType  # avoiding runtime costs
```


YOU SHOULD NOT use `typing.Any` if it is possible to narrow the type to something more specific.
YOU SHOULD NOT silence the type checker with `type: ignore` unless other options are exhausted. Consider first using `typing.cast` or refactoring the code. If you must use a `type: ignore`, try to be specific in what error code you're ignoring and leave a comment with a link or explanation so that it may be rectified later.

```python
# type: ignore[misc]  # mypy ignores only the error code in brackets

# pyright: ignore[reportPrivateUsage]  # pyright ignores only the error code in brackets

# type: ignore  # all errors ignored by both mypy and pyright
```

DO mark a parameter as `typing.Optional` if an explicit value of `None` is allowed.

```python
from typing import Optional

def foo(
    bar: str = "baz",  # Arg with a default, doesn't allow None
    bat: Optional[str] = None,  # None is allowed, type as Optional
) -> None:
    ...
```

DO use `typing.Union` when a parameter can accept more than one type.
DO specify type parameters for collection types. If not specified, these will be assumed as `Any`.

```python
# No:
def get_entity(entity_id) -> dict:  # seen by type checker as dict[Any, Any]
    ...

# Yes:
def get_entity(entity_id: str) -> dict[str, str]:
    ...

```
YOU SHOULD be lenient in what you accept as a parameter. For example, typing a parameter as accepting Sequence over List, or Mapping over Dict gives flexibility to the caller.
Ensure that the type hint given for the parameter supports the set of operations needed in the function body.

```python
from typing import Sequence, Iterable

# Yes:
def create_batch(entities: Sequence[Entity]) -> None:
    if len(entities) > 1:
        ...

# No: the function calls len(), Iterable doesn't support it
def create_batch(entities: Iterable[Entity]) -> None:
    if len(entities) > 1:
        ...
```

DO use `typing.TypedDict` if the dictionary has a fixed set of keys.

```python
from typing_extensions import TypedDict

class Employee(TypedDict):
    name: str
    title: str
    id: int
    current: bool
```

DO use `from __future__ import annotations` for forward declarations or when using built-in generic collection types, like `dict` or `list`.

```python
from __future__ import annotations  # must be first import in file

class Triangle:

    @classmethod
    def from_shape(cls) -> Triangle: # Don't need to make Triangle a forward reference / string
        ...

    def get_points(self) -> list[float]:  # allows use of list instead of typing.List
        ...
```

DO use type aliases to help make lengthy, complicated type hints more readable and help convey meaning to the reader.

```python
from typing import Union
from azure.core.credentials import AzureKeyCredential, TokenCredential, AzureSasCredential

CredentialTypes = Union[AzureKeyCredential, TokenCredential, AzureSasCredential]  # PascalCase
```

DO use `typing.overload` if your function takes different combinations or types of arguments and/or the input arguments inform the return type.
DO support the "duck typing" of Python with `typing.Protocol`.
DO mark your `typing.Protocol`s as `@runtime_checkable`.

DO give your `typing.TypeVar`'s descriptive names if they will be publicly exposed in the code.

```python
from typing import TypeVar, Generic

# No:
T = TypeVar("T")

class LROPoller(Generic[T]):
    ...

# Yes:
PollingReturnType = TypeVar("PollingReturnType")

class LROPoller(Generic[PollingReturnType]):
    ...
```

DO follow naming conventions for covariant (*_co) and contravariant (*_contra) TypeVar parameters.

```python
from typing import TypeVar

T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)
```