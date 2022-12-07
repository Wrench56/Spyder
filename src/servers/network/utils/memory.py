import sys
import ctypes

# From: https://stackoverflow.com/questions/982682/mark-data-as-sensitive-in-python/983525#983525
def erase_variable(var):
    location = id(var) + 20
    size = sys.getsizeof(var) - 20

    ctypes.memset(location, 0, size)
    del var