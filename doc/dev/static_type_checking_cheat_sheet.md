

- DO use mypy and pyright type checkers to statically type check your client library code.
- DO NOT use comment style type hints. Use inline, annotation style.
- DO mark your client library package to distribute type hints according to [PEP 561](https://peps.python.org/pep-0561/)
- Do type annotate anything in the client library that is customer facing / public API.
- DO use the latest typing features available. If not supported by older versions of Python, consider importing from `typing-extensions`.
- Do not import types from `typing` or `typing-extensions` under a `typing.TYPE_CHECKING` block -- this isn't necessary.
- DO not use `typing.Any` if it is possible to narrow the type to something more specific.
- You should not use `type: ignore` unless all other options are exhausted. Consider using `cast` or refactoring the code. If you must use a `type: ignore`, be specific in what you're ignoring and leave a comment so that it may be rectified later.
- DO use type aliases to help make lengthy, unwieldly type hints more readable and help convey meaning to types.
- DO use `typing.overload` if your function takes different combinations or types of arguments and/or the input arguments inform the return type.
- Do support the "duck typing" of Python with `typing.Protocol`.
- Do mark your `typing.Protocol`s as `@runtime_checkable`
- You should be lenient in what you accept as a parameter. E.g. type things as accepting Sequence over List, or Mapping over Dict. This gives flexibility to the caller.
- Do mark a parameter as `typing.Optional` if an explicit value of `None` is allowed.
- Do use `typing.Union` for parameter types, but try to avoid as a return type.
