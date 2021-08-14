# -*- coding: utf-8 -*-
#
# Package defines.
# Customize them according to your needs and supplied hardware
# 
# 
#
# pylint: disable=no-member
# pylint: disable=import-error
#
VERSION = "1.0"
YAML_DEFAULT = 'config.yaml'

# Display
DISPLAY_FRAMEBUFFER = "/dev/fb1"
DISPLAY_DRIVER = "fbcon"            # fbcon|directfb|svgalib

# Keyboard-GPIO
KEY1      = 12
KEY2      = 16
KEY3      = 18
KEY_UP    = KEY1
KEY_DOWN  = KEY2
KEY_ENTER = KEY3

# Touch device
TOUCH_DEV = "/dev/input/touchscreen"

# Display driver currently used, PICKUP '_ONE_' OF THEM
# from pysplay.display_waveshare import displayDriver         # Waveshare TFT SPI display
from pysplay.display_waveshare import displayDriver         # Waveshare TFT SPI display

SCREEN_CALIBRATION = {'display': [
                            {'type': 'crosshair', 'x': 160, 'y': 120, 'radius': 15, 'color': '0,0,255'},
                            {'type': 'crosshair', 'x': 0,   'y': 0,   'radius': 15},
                            {'type': 'crosshair', 'x': 0,   'y': 239, 'radius': 15},
                            {'type': 'crosshair', 'x': 319, 'y': 239, 'radius': 15},
                            {'type': 'crosshair', 'x': 319, 'y': 0,   'radius': 15}
                      ],
                      'width': 320,
                      'height': 240
                     }
# OUTPUT #
# 1> A=2041   B=1951
# 2> A=246    B=3794
# 3> A=3772   B=3817
# 4> A=3807   B=226
# 5> A=198    B=206
#    [(2041, 1951), (246, 3794), (3772, 3817), (3807, 226), (198, 206)]
# 
# 'width': 320,         # X -> -B
# 'height': 240,        # Y -> +A
#  X = 216,3805         # X-Ratio 320/3805 ~= 0.08  # M=(3805-216)/2+216 ~= 2010
#  Y = 222,3789         # Y-Ratio 240/3789 ~= 0.06  # M=(3789-222)/2+222 ~= 2005
#
# Fix ratio according to your screen, ALWAYS
getRawCoord = lambda a,b: (b, a)                                # Get raw touchscreen coords
getCoord    = lambda a,b: (320-int(0.083*b), int(0.06*a))       # Touch coordinates -> pixels

coordToTouch = lambda x,y: (int((320-x)/0.083), int(y/0.06))    # Pixels -> Touch coordinates
