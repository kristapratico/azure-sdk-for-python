from .computer_vision_client import ComputerVisionClient
from ._policies import CognitiveServicesCredentialPolicy
from ._polling import ComputerVisionPollingMethod
__all__ = ['ComputerVisionClient', 'CognitiveServicesCredentialPolicy', 'ComputerVisionPollingMethod']

from .version import VERSION

__version__ = VERSION
