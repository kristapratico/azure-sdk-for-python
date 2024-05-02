# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------


from ._version import VERSION

__version__ = VERSION

from ._trace import InstrumentOpenAI

__all__ = ["InstrumentOpenAI"]