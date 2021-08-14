# -*- coding: utf-8 -*-
#
# pylint: disable=no-member
# pylint: disable=import-error
#
import evdev
#
import pysplay.const as const


# Touchscreen class
class touchscreen():
    def __init__(self):
        self._device = evdev.InputDevice(const.TOUCH_DEV)

    def eventLoop(self):
        return self._device.read_loop()

    def close(self):
        self._device.close()

    @property
    def open(self):
        if self._device.fd > 0:
            return True
        return False
