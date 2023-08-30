# pylint: disable=protected-access

from typing import Tuple
import sys


# Note: The sys wiki states that "It (sys._getframe())
#       is not guranteed to exist in all
#       implementations of Python"
def get_caller(depth: int = 1) -> Tuple[str, str]:
    frame = sys._getframe(depth)
    return (frame.f_globals['__name__'],
            frame.f_code.co_name)
