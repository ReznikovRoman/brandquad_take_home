from .base import Base
from .lint import Lint

try:
    from .local import Local
except ImportError:
    LOCAL_CONFIGURATION_EXISTS = False
else:
    LOCAL_CONFIGURATION_EXISTS = True

__all__ = [
    "Base",
    "Lint",
]

if LOCAL_CONFIGURATION_EXISTS:
    __all__ += ["Local"]
