#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""High-level interface to a opus decoder functions"""

__author__ = 'Никита Кузнецов <self@svartalf.info>'
__copyright__ = 'Copyright (c) 2012, SvartalF'
__license__ = 'BSD 3-Clause License'


import opuslib.api


class Decoder(object):

    def __init__(self, fs, channels):
        """
        Parameters:
            fs : sampling rate
            channels : number of channels
        """

        self._fs = fs
        self._channels = channels
        self._state = opuslib.api.decoder.create(fs, channels)

    def __del__(self):
        if hasattr(self, '_state'):
            # Destroying state only if __init__ completed successfully
            opuslib.api.decoder.destroy(self._state)

    def reset_state(self):
        """
        Resets the codec state to be equivalent to a freshly initialized state
        """

        opuslib.api.decoder.opuslib.api.ctl(
            self._state, opuslib.api.ctl.reset_state)

    def decode(self, data, frame_size, decode_fec=False):
        return opuslib.api.decoder.decode(
            self._state, data, len(data), frame_size, decode_fec,
            channels=self._channels)

    def decode_float(self, data, frame_size, decode_fec=False):
        return opuslib.api.decoder.decode_float(
            self._state, data, len(data), frame_size, decode_fec,
            channels=self._channels)

    # CTL interfaces

    _get_final_range = lambda self: opuslib.api.decoder.opuslib.api.ctl(
        self._state, opuslib.api.ctl.get_final_range)

    final_range = property(_get_final_range)

    _get_bandwidth = lambda self: opuslib.api.decoder.opuslib.api.ctl(
        self._state, opuslib.api.ctl.get_bandwidth)

    bandwidth = property(_get_bandwidth)

    _get_pitch = lambda self: opuslib.api.decoder.opuslib.api.ctl(
        self._state, opuslib.api.ctl.get_pitch)

    pitch = property(_get_pitch)

    _get_lsb_depth = lambda self: opuslib.api.decoder.opuslib.api.ctl(
        self._state, opuslib.api.ctl.get_lsb_depth)

    _set_lsb_depth = lambda self, x: opuslib.api.decoder.opuslib.api.ctl(
        self._state, opuslib.api.ctl.set_lsb_depth, x)

    lsb_depth = property(_get_lsb_depth, _set_lsb_depth)

    _get_gain = lambda self: opuslib.api.decoder.opuslib.api.ctl(
        self._state, opuslib.api.ctl.get_gain)

    _set_gain = lambda self, x: opuslib.api.decoder.opuslib.api.ctl(
        self._state, opuslib.api.ctl.set_gain, x)

    gain = property(_get_gain, _set_gain)
