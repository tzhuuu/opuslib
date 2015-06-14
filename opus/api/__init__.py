import ctypes
from ctypes.util import find_library

lib_location = find_library('opus')
if lib_location is None:
    raise FileNotFoundError("Could not find opus library. Make sure it is installed")
libopus = ctypes.CDLL(lib_location)

c_int_pointer = ctypes.POINTER(ctypes.c_int)
c_int16_pointer = ctypes.POINTER(ctypes.c_int16)
c_float_pointer = ctypes.POINTER(ctypes.c_float)
