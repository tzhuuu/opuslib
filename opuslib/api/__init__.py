#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
#

"""OpusLib Package."""

import ctypes  # type: ignore
import os
import sys
from ctypes.util import find_library  # type: ignore

__author__ = 'Никита Кузнецов <self@svartalf.info>'
__copyright__ = 'Copyright (c) 2012, SvartalF'
__license__ = 'BSD 3-Clause License'

libopus = None


def _load_default():
    global libopus
    if sys.platform == 'win32':
        _basedir = os.path.dirname(os.path.abspath(__file__))
        _bitness = 'x64' if sys.maxsize > 2 ** 32 else 'x86'
        _filename = os.path.join(_basedir, 'bin', 'libopus-0.{}.dll'.format(_bitness))
        libopus = _libopus_loader(_filename)
    else:
        lib_location = find_library('opus')
        if lib_location is None:
            raise Exception(
                'Could not find Opus library. Make sure it is installed.')

        libopus = _libopus_loader(lib_location)


def _libopus_loader(name):
    # create the library...
    lib = ctypes.cdll.LoadLibrary(name)
    return lib


_load_default()

c_int_pointer = ctypes.POINTER(ctypes.c_int)
c_int16_pointer = ctypes.POINTER(ctypes.c_int16)
c_float_pointer = ctypes.POINTER(ctypes.c_float)
