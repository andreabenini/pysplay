# -*- coding: utf-8 -*-
#
# pylint: disable=no-member
# pylint: disable=import-error
#
import time
import pygame

import pysplay.utility
from pysplay.const import displayDriver
from pysplay.const import SCREEN_CALIBRATION


# Display class
class display(displayDriver):
    def __init__(self, screen):
        # Init display
        displayDriver.__init__(self)        # self._screen -> self.screen (Inherited property)

    @property
    def screen(self):
        return self._screen

    # Clear screen,  black
    def clear(self):
        self._screen.fill((0,0,0))

    # Update the screen
    def update(self):
        pygame.display.update()
        time.sleep(0.1)

    # Display a "please wait" screen
    def wait(self, text='...please wait...'):
        self.clear()
        self.showText({
            'x': int(SCREEN_CALIBRATION['width']/2),
            'y': int(SCREEN_CALIBRATION['height']/2)-24,
            'text': text,
            'textsize': 24,
            'textfont': 'freesans',
            'textalign': 'center',
            'textcolor': (255,255,255)
        })
        self.update()

    # Display a screen
    def show(self, screen):
        for item in screen['display']:
            self.widgetShow(item, refresh=False)
        self.update()

    # Draw a widget
    def widgetShow(self, widget, refresh=True):
        if   widget['type'] == 'crosshair':
            self.showCrosshair(widget)
        elif widget['type'] == 'circle':
            self.showCircle(widget)
        elif widget['type'] == 'box':
            self.showBox(widget)
        elif widget['type'] == 'image':
            self.showImage(widget)
        elif widget['type'] == 'button':
            self.showButton(widget)
        elif widget['type'] == 'listbox':
            self.showListbox(widget)
        elif widget['type'] == 'windowdialog':
            self.showWindowDialog(widget)
        elif widget['type'] == 'text':
            self.showText(widget)
        elif widget['type'] == 'dot':
            self.showDot(widget)
        if refresh:
            self.update()

    # Clear previous widget and redraw a new one on behalf
    def widgetRefresh(self, widgetOld=None, widgetNew=None, refresh=True):
        if widgetOld['type'] == 'text':
            self.refreshText(widgetOld, widgetNew)
        else:
            self.widgetShow(widgetNew, refresh=False)
        if refresh:
            self.update()
