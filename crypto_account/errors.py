from enum import Enum, auto


class CryptoAccountError(Enum):
    CONNECTION_ERROR = auto()
    INVALID_INPUT_PARAMETERS = auto()
    UNKNOWN_ERROR = auto()
