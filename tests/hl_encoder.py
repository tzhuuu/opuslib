#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for a high-level Decoder object"""

import unittest

import opuslib

__author__ = 'Никита Кузнецов <self@svartalf.info>'
__copyright__ = 'Copyright (c) 2012, SvartalF'
__license__ = 'BSD 3-Clause License'


class EncoderTest(unittest.TestCase):

    def test_create(self):
        try:
            opuslib.Encoder(1000, 3, opuslib.APPLICATION_AUDIO)
        except opuslib.OpusError as ex:
            self.assertEqual(ex.code, opuslib.BAD_ARG)

        opuslib.Encoder(48000, 2, opuslib.APPLICATION_AUDIO)

    def test_reset_state(self):
        encoder = opuslib.Encoder(48000, 2, opuslib.APPLICATION_AUDIO)
        encoder.reset_state()
