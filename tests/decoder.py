#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import unittest

import opuslib.api
import opuslib.api.decoder
import opuslib.api.ctl

__author__ = 'Никита Кузнецов <self@svartalf.info>'
__copyright__ = 'Copyright (c) 2012, SvartalF'
__license__ = 'BSD 3-Clause License'


class DecoderTest(unittest.TestCase):
    """Decoder basic API tests

    From the `tests/test_opus_api.c`
    """

    def test_get_size(self):
        """Invalid configurations which should fail"""

        for c in range(4):
            i = opuslib.api.decoder.libopus_get_size(c)
            if c in (1, 2):
                self.assertFalse(1 << 16 < i <= 2048)
                pass
            else:
                self.assertEqual(i, 0)

    def _test_unsupported_sample_rates(self):
        """
        Unsupported sample rates

        TODO: make the same test with a opus_decoder_init() function
        """
        for c in range(4):
            for i in range(-7, 96000):
                if i in (8000, 12000, 16000, 24000, 48000) and c in (1, 2):
                    continue

                if i == -5:
                    fs = -8000
                elif i == -6:
                    fs = sys.maxsize  # TODO: should be a INT32_MAX
                elif i == -7:
                    fs = -1 * (sys.maxsize - 1)  # Emulation of the INT32_MIN
                else:
                    fs = i

                try:
                    dec = opuslib.api.decoder.create_state(fs, c)
                except opuslib.OpusError as e:
                    self.assertEqual(e.code, opuslib.BAD_ARG)
                else:
                    decoder.destroy(dec)

    def test_create(self):
        try:
            dec = opuslib.api.decoder.create_state(48000, 2)
        except opuslib.OpusError:
            raise AssertionError()
        else:
            opuslib.api.decoder.destroy(dec)


            # TODO: rewrite this code
        # VG_CHECK(dec,opus_decoder_get_size(2));

    def test_get_final_range(self):
        dec = opuslib.api.decoder.create_state(48000, 2)
        opuslib.api.decoder.decoder_ctl(dec, opuslib.api.ctl.get_final_range)
        opuslib.api.decoder.destroy(dec)

    def test_unimplemented(self):
        dec = opuslib.api.decoder.create_state(48000, 2)
        try:
            opuslib.api.decoder.decoder_ctl(
                dec, opuslib.api.ctl.unimplemented)
        except opuslib.OpusError as xe:
            self.assertEqual(xe.code, opuslib.UNIMPLEMENTED)
        opuslib.api.decoder.destroy(dec)

    def test_get_bandwidth(self):
        dec = opuslib.api.decoder.create_state(48000, 2)
        value = opuslib.api.decoder.decoder_ctl(dec, opuslib.api.ctl.get_bandwidth)
        self.assertEqual(value, 0)
        opuslib.api.decoder.destroy(dec)

    def test_get_pitch(self):
        dec = opuslib.api.decoder.create_state(48000, 2)

        i = opuslib.api.decoder.decoder_ctl(dec, opuslib.api.ctl.get_pitch)
        self.assertIn(i, (-1, 0))

        packet = bytes([252, 0, 0])
        opuslib.api.decoder.decode(dec, packet, 3, 960, False)
        i = opuslib.api.decoder.decoder_ctl(dec, opuslib.api.ctl.get_pitch)
        self.assertIn(i, (-1, 0))

        packet = bytes([1, 0, 0])
        opuslib.api.decoder.decode(dec, packet, 3, 960, False)
        i = opuslib.api.decoder.decoder_ctl(dec, opuslib.api.ctl.get_pitch)
        self.assertIn(i, (-1, 0))

        opuslib.api.decoder.destroy(dec)

    def test_gain(self):
        dec = opuslib.api.decoder.create_state(48000, 2)

        i = opuslib.api.decoder.decoder_ctl(dec, opuslib.api.ctl.get_gain)
        self.assertEqual(i, 0)

        try:
            opuslib.api.decoder.decoder_ctl(dec, opuslib.api.ctl.set_gain, -32769)
        except opuslib.OpusError as e:
            self.assertEqual(e.code, opuslib.BAD_ARG)

        try:
            opuslib.api.decoder.decoder_ctl(dec, opuslib.api.ctl.set_gain, 32768)
        except opuslib.OpusError as e:
            self.assertEqual(e.code, opuslib.BAD_ARG)

        opuslib.api.decoder.decoder_ctl(dec, opuslib.api.ctl.set_gain, -15)
        i = opuslib.api.decoder.decoder_ctl(dec, opuslib.api.ctl.get_gain)
        self.assertEqual(i, -15)

        opuslib.api.decoder.destroy(dec)

    def test_reset_state(self):
        dec = opuslib.api.decoder.create_state(48000, 2)
        opuslib.api.decoder.decoder_ctl(dec, opuslib.api.ctl.reset_state)
        opuslib.api.decoder.destroy(dec)

    def test_get_nb_samples(self):
        """opus_decoder_get_nb_samples()"""

        dec = opuslib.api.decoder.create_state(48000, 2)

        self.assertEqual(
            480, opuslib.api.decoder.get_nb_samples(dec, bytes([0]), 1))

        packet = ''.join([chr(x) for x in ((63 << 2)|3, 63)])
        packet = bytes()
        for x in ((63 << 2)|3, 63):
            packet += bytes([x])

        # TODO: check for exception code
        self.assertRaises(
            opuslib.OpusError,
            lambda: opuslib.api.decoder.get_nb_samples(dec, packet, 2)
        )

        opuslib.api.decoder.destroy(dec)


    def test_packet_get_nb_frames(self):
        """opus_packet_get_nb_frames()"""

        packet = ''.join([chr(x) for x in ((63 << 2)|3, 63)])
        packet = bytes()
        for x in ((63 << 2)|3, 63):
            packet += bytes([x])

        self.assertRaises(
            opuslib.OpusError,
            lambda: opuslib.api.decoder.packet_get_nb_frames(packet, 0)
        )

        l1res = (1, 2, 2, opuslib.INVALID_PACKET)

        for i in range(0, 256):
            packet = bytes([i])
            expected_result = l1res[i & 3]

            try:
                self.assertEqual(
                    expected_result,
                    opuslib.api.decoder.packet_get_nb_frames(packet, 1)
                )
            except opuslib.OpusError as ex:
                if ex.code == expected_result:
                    continue

            for j in range(0, 256):
                packet = bytes([i, j])

                self.assertEqual(
                    expected_result if expected_result != 3 else (packet[1] & 63),
                    opuslib.api.decoder.packet_get_nb_frames(packet, 2)
                )

    def test_packet_get_bandwidth(self):
        """opus_packet_get_bandwidth()"""

        for i in range(0, 256):
            packet = bytes([i])
            bw = i >> 4

            # Very cozy code from the test_opus_api.c
            bw = opuslib.BANDWIDTH_NARROWBAND + (((((bw & 7) * 9) & (63 - (bw & 8))) + 2 + 12 * ((bw & 8) != 0)) >> 4)

            self.assertEqual(
                bw, opuslib.api.decoder.packet_get_bandwidth(packet)
            )

    def test_decode(self):
        """opus_decode()"""

        packet = bytes([255, 49])
        for j in range(2, 51):
            packet += bytes([0])

        dec = opuslib.api.decoder.create_state(48000, 2)
        try:
            opuslib.api.decoder.decode(dec, packet, 51, 960, 0)
        except opuslib.OpusError as ex:
            self.assertEqual(ex.code, opuslib.INVALID_PACKET)

        packet = bytes([252, 0, 0])
        try:
            opuslib.api.decoder.decode(dec, packet, -1, 960, 0)
        except opuslib.OpusError as ex:
            self.assertEqual(ex.code, opuslib.BAD_ARG)

        try:
            opuslib.api.decoder.decode(dec, packet, 3, 60, 0)
        except opuslib.OpusError as ex:
            self.assertEqual(ex.code, opuslib.BUFFER_TOO_SMALL)

        try:
            opuslib.api.decoder.decode(dec, packet, 3, 480, 0)
        except opuslib.OpusError as ex:
            self.assertEqual(ex.code, opuslib.BUFFER_TOO_SMALL)

        try:
             opuslib.api.decoder.decode(dec, packet, 3, 960, 0)
        except opuslib.OpusError:
            self.fail('Decode failed')

        opuslib.api.decoder.destroy(dec)

    def test_decode_float(self):
        dec = opuslib.api.decoder.create_state(48000, 2)

        packet = bytes([252, 0, 0])

        try:
            opuslib.api.decoder.decode_float(dec, packet, 3, 960, 0)
        except opuslib.OpusError:
            self.fail('Decode failed')

        opuslib.api.decoder.destroy(dec)
