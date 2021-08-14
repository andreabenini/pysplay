# -*- coding: utf-8 -*-
#
# pylint: disable=no-member
# pylint: disable=import-error
#
import evdev
import multiprocessing

import pysplay.const
import pysplay.touchscreen


# System class with project resources
class event():
    def __init__(self, messageQueue):
        self._touch = pysplay.touchscreen()
        self._messageQueue = messageQueue
        self._eventDetected()

    @property   # [events] object
    def events(self):
        return self._touch.eventLoop()

    @property   # Are there any events in the queue ?
    def hasevents(self):
        return self._touch.open

    # Main event loop
    def eventLoop(self):
        message = {'type': 'event', 'data': None}
        try:
            for event in self.events:
                (X,Y) = self._eventGet(event)
                if X:
                    message['data'] = (X, Y)
                    self._messageQueue.put(message)
        except Exception:
            print("eventLoop() error")


    # Init event queue
    def _eventDetected(self, touch=False):
        self._eventX = self._eventY = -1
        self._eventTouchDetected = touch

    # Reading a single coordinate from event queue, if available and valid
    def _eventGetCoord(self, event, code, value):
        if event.type == evdev.ecodes.EV_ABS and event.code == code and value==-1 and self._eventTouchDetected:
            return evdev.categorize(event).event.value
        return value


    # Detect current event
    def _eventGet(self, event):
        X = Y = None
        # Detect touch key_down
        if event.type==evdev.ecodes.EV_KEY and event.code==evdev.ecodes.BTN_TOUCH and event.value==evdev.events.KeyEvent.key_down:
            self._eventDetected(True)
        # Releasing touch even upon SYN_REPORT
        if event.type == evdev.ecodes.EV_SYN and event.code == evdev.ecodes.SYN_REPORT:
            if event.value==evdev.events.KeyEvent.key_up and self._eventTouchDetected:
                (X,Y) = pysplay.const.getRawCoord(self._eventX, self._eventY)
            self._eventDetected()
        # Reading Coords if [self._eventTouchDetected]
        self._eventX = self._eventGetCoord(event, evdev.ecodes.ABS_X, self._eventX)
        self._eventY = self._eventGetCoord(event, evdev.ecodes.ABS_Y, self._eventY)
        return (X, Y)


def eventProcess(messageQueue):
    eventManager = event(messageQueue)
    eventManager.eventLoop()
