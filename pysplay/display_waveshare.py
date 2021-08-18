# -*- coding: utf-8 -*-
#
# pylint: disable=no-member
# pylint: disable=import-error
#
import os
import pygame
# Package defines
import pysplay.const as const


# Display driver class
class displayDriver():
    def __init__(self):
        # Framebuffer device
        os.environ["DISPLAY"] = ":0.0"
        os.environ["SDL_FBDEV"]       = const.DISPLAY_FRAMEBUFFER
        os.environ["SDL_VIDEODRIVER"] = const.DISPLAY_DRIVER
        # Touchscreen
        os.environ["SDL_MOUSEDRV"]    = "TSLIB"
        os.environ["SDL_MOUSEDEV"]    = const.TOUCH_DEV
        # Display init
        pygame.init()
        pygame.display.init()
        pygame.mouse.set_visible(False)
        DisplaySize = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self._screen = pygame.display.set_mode(DisplaySize, pygame.NOFRAME)
        pygame.display.set_caption('pysplaylib')
        # Loading fonts   ['dejavuserif', 'dejavusansmono', 'freesans', 'dejavusans', 'freeserif', 'freemono']
        # self.fontTitle = pygame.font.Font('freesansbold.ttf', 16)
        self.fontTitle  = pygame.font.SysFont('freesansbold', 18)
        self.fontButton = {'name': 'freesansbold', 'size': 12}
        self.fontText   = pygame.font.SysFont('freesans', 16)
        self.fontInfo   = pygame.font.Font('freesansbold.ttf', 12)

    # fontName = ['dejavuserif', 'dejavusansmono', 'freesans', 'dejavusans', 'freeserif', 'freemono']
    def font(self, Font={'name': 'freesans', 'size': 12}):
        return self._font(fontName=Font['name'], size=Font['size'])
    def _font(self, size=10, fontName='freesans'):
        return pygame.font.SysFont(fontName, size)

    # Draw a circle
    def showCircle(self, circle):
        pygame.draw.circle(self._screen, circle['color'], (circle['x'],circle['y']), circle['radius'], 0 if circle['fill'] else 1)

    # Draw a crosshair (useful for calibration)
    def showCrosshair(self, crosshair):
        self.showCircle(crosshair)
        if not crosshair['fill']:
            pygame.draw.line(self._screen,   crosshair['color'], (crosshair['x']-crosshair['radius'] ,crosshair['y']), (crosshair['x']+crosshair['radius'], crosshair['y']), 1)
            pygame.draw.line(self._screen,   crosshair['color'], (crosshair['x'], crosshair['y']-crosshair['radius']), (crosshair['x'], crosshair['y']+crosshair['radius']), 1)

    # Draw a box
    def showBox(self, box):
        rectangle = pygame.Rect((box['x'], box['y']), (box['width'], box['height']))    # pos, size
        pygame.draw.rect(self._screen, box['color'], rectangle)
        if box['border'] > 0:
            pygame.draw.line(self._screen, box['bordercolor'], (box['x'], box['y']), (box['x']+box['width']-box['border'], box['y']), box['border'])
            pygame.draw.line(self._screen, box['bordercolor'], (box['x'], box['y']), (box['x'], box['y']+box['height']-box['border']), box['border'])
            pygame.draw.line(self._screen, box['bordercolor'], (box['x']+box['width']-box['border'], box['y']), (box['x']+box['width']-box['border'], box['y']+box['height']-box['border']), box['border'])
            pygame.draw.line(self._screen, box['bordercolor'], (box['x'], box['y']+box['height']-box['border']), (box['x']+box['width']-box['border'], box['y']+box['height']-box['border']), box['border'])

    # Draw a button
    def showButton(self, button, buttonFont=None):
        # Box
        rectangle = pygame.Rect((button['x'], button['y']), (button['width'], button['height']))    # pos, size
        pygame.draw.rect(self._screen, button['color'], rectangle)
        # Border
        if button['border'] > 0:
            pygame.draw.line(self._screen, button['textcolor'], (button['x'], button['y']), (button['x']+button['width']-button['border'], button['y']), button['border'])
            pygame.draw.line(self._screen, button['textcolor'], (button['x'], button['y']), (button['x'], button['y']+button['height']-button['border']), button['border'])
            pygame.draw.line(self._screen, button['bordercolor'], (button['x']+button['width']-button['border'], button['y']), (button['x']+button['width']-button['border'], button['y']+button['height']-button['border']), button['border'])
            pygame.draw.line(self._screen, button['bordercolor'], (button['x'], button['y']+button['height']-button['border']), (button['x']+button['width']-button['border'], button['y']+button['height']-button['border']), button['border'])
        # Button Text
        if buttonFont == None:
            fontAttributes = {'name': self.fontButton['name'], 'size': button['textsize']}
            buttonFont = self.font(fontAttributes)
        fontImage = buttonFont.render(button['text'], 1, button['textcolor'])
        w,h = buttonFont.size(button['text'])
        if button['textalign'] == 'left':
            textPos = (button['x']+button['textspacing'],   button['y']+button['height']/2-h/2)
        elif button['textalign'] == 'right':
            textPos = (button['x']+button['width']-button['textspacing'], button['y']+button['height']/2-h/2)
        else:
            textPos = (button['x']+button['width']/2-w/2,   button['y']+button['height']/2-h/2)
        self._screen.blit(fontImage, textPos)


    # Display an image
    def showImage(self, item):
        image = pygame.image.load(item['src'])
        self._screen.blit(image, (item['x'], item['y']))

    # Refresh an image on screen. Clear the old one (with a box) and display the newer
    def refreshImage(self, widgetOld, widgetNew):
        image = pygame.image.load(widgetNew['src'])
        rectangle = image.get_rect()
        pygame.draw.rect(self._screen, widgetOld['color'], rectangle.move( (widgetNew['x'],widgetNew['y']) ))
        self._screen.blit(image, (widgetNew['x'],widgetNew['y']))


    # Write a text
    def showText(self, text, customFont=None):
        if customFont:
            font = customFont
        else:
            font = self._font(size=text['textsize'], fontName=text['textfont'])
        fontImage = font.render(text['text'], 1, text['textcolor'])
        w,_ = font.size(text['text'])                               # size of font image
        if text['textalign'] == 'left':
            textPos = (text['x'],     text['y'])                    # left alignment
        elif text['textalign'] == 'right':
            textPos = (text['x']-w,   text['y'])                    # right alignment
        else:
            textPos = (text['x']-w/2, text['y'])                    # center alignment
        self._screen.blit(fontImage, textPos)

    def refreshText(self, textOld, textNew, customFont=None):
        # Erase previous text
        if customFont:
            font = customFont
        else:
            font = self._font(size=textOld['textsize'], fontName=textOld['textfont'])
        width, heigth = font.size(textOld['text'])      # size of previous font image
        if textOld['textalign'] == 'left':
            x = textOld['x']                            # left alignment
        elif textOld['textalign'] == 'right':
            x = textOld['x']-width                      # right alignment
        else:
            x = textOld['x']-width/2                    # center alignment
        self.showBox({
            'x': x,
            'y': textOld['y'],
            'width': width,
            'height': heigth,
            'color': textOld['textcolor'],
            'border': 0
        })
        # Draw new text
        self.showText(textNew, customFont)


    # Draw a dot/pixel on screen
    def showDot(self, dot):
        self._screen.set_at((dot['x'], dot['y']), dot['color'])

    def showListbox(self, item):
        # Widget box
        widgetBox = pygame.Rect((item['x']+item['border'], item['y']+item['border']), (item['width']-item['border'], item['height']-item['border']))
        pygame.draw.rect(self._screen, item['color'], widgetBox)
        if (item['border']>0):
            pygame.draw.line(self._screen, item['bordercolor'],     # Top
                         (item['x'], item['y']), (item['x']+item['width'], item['y']), item['border'])
            pygame.draw.line(self._screen, item['bordercolor'],     # Bottom
                         (item['x'], item['y']+item['height']), (item['x']+item['width'], item['y']+item['height']), item['border'])
            pygame.draw.line(self._screen, item['bordercolor'],     # Left
                         (item['x'], item['y']), (item['x'], item['y']+item['height']), item['border'])
            pygame.draw.line(self._screen, item['bordercolor'],     # Right
                         (item['x']+item['width'], item['y']), (item['x']+item['width'], item['y']+item['height']), item['border'])
        # Items list
        x = item['x']+item['textspacing']
        y = item['y']+item['textspacing']/2
        i = item['start']
        drawScrollBar = False if item['start'] <= 0 else True
        while i < len(item['list']):         # Iterate through items
            self.showText({
                'x': x,
                'y': y,
                'text': item['list'][i]['text'],
                'textsize': item['textsize'],
                'textfont': item['textfont'],
                'textcolor': item['list'][i]['color'],
                'textalign': item['textalign']
            })
            y += item['textsize']
            if y+item['textsize'] >= item['y']+item['height']:
                i = len(item['list'])
                drawScrollBar = True                # Not enough space, a scroll bar is needed
            else:
                i += 1
        # Draw the scrollbar
        if drawScrollBar and item['scrollbarwidth'] > 0:
            pygame.draw.line(self._screen, item['bordercolor'],             # Scrollbar vertical line separator
                                (item['x']+item['width']-item['scrollbarwidth'], item['y']),
                                (item['x']+item['width']-item['scrollbarwidth'], item['y']+item['height']),
                                item['border'])
            pygame.draw.line(self._screen, item['bordercolor'],             # Scrollbar horizontal line separator
                                (item['x']+item['width']-item['scrollbarwidth'], item['y']+item['height']/2),
                                (item['x']+item['width'], item['y']+item['height']/2),
                                item['border'])
            pygame.draw.polygon(self._screen, item['bordercolor'],          # Scrollbar arrow up
                                [ (item['x']+item['width']-item['scrollbarwidth']/2, item['y']+item['textspacing']),
                                  (item['x']+item['width']-item['scrollbarwidth']/2-item['textspacing'], item['y']+item['textspacing']*2),
                                  (item['x']+item['width']-item['scrollbarwidth']/2+item['textspacing'], item['y']+item['textspacing']*2) ],
                                item['border'])
            pygame.draw.polygon(self._screen, item['bordercolor'],          # Scrollbar arrow down
                                [ (item['x']+item['width']-item['scrollbarwidth']/2, item['y']+item['height']-item['textspacing']),
                                  (item['x']+item['width']-item['scrollbarwidth']/2-item['textspacing'], item['y']+item['height']-item['textspacing']*2),
                                  (item['x']+item['width']-item['scrollbarwidth']/2+item['textspacing'], item['y']+item['height']-item['textspacing']*2) ],
                                item['border'])


    # Draw a window message dialog
    def showWindowDialog(self, item):
        # Title
        fontTitle = self.fontTitle
        _, titleHeight = fontTitle.size(item['title'])
        titleHeight += 6
        fontTitleImage = fontTitle.render(item['title'], 1, item['textcolor'])
        titlePos = (item['x']+10, item['y']+3)
        # Title box
        titlebox = pygame.Rect((item['x'], item['y']), (item['width']-1, titleHeight))
        pygame.draw.rect(self._screen, item['titlebackground'], titlebox)
        self._screen.blit(fontTitleImage, titlePos)
        pygame.draw.line(self._screen, item['buttoncolor'], (item['x'], item['y']+titleHeight-1), (item['x']+item['width']-1, item['y']+titleHeight-1), 1)
        # Main Window Box
        rectangle = pygame.Rect((item['x'], item['y']+titleHeight), (item['width']-1, item['height']-1))
        pygame.draw.rect(self._screen, item['color'], rectangle)
        pygame.draw.line(self._screen, item['bordercolor'],             # Top
                         (item['x'], item['y']), (item['x']+item['width']-1, item['y']), 1)
        pygame.draw.line(self._screen, item['bordercolor'],             # Bottom
                         (item['x'], item['y']+item['height']+titleHeight-1), (item['x']+item['width']-1, item['y']+item['height']+titleHeight-1), 1)
        pygame.draw.line(self._screen, item['bordercolor'],             # Left
                         (item['x'], item['y']), (item['x'], item['y']+item['height']+titleHeight-1), 1)
        pygame.draw.line(self._screen, item['bordercolor'],             # Right
                         (item['x']+item['width']-1, item['y']), (item['x']+item['width']-1, item['y']+item['height']+titleHeight-1), 1)
        # Window Text
        self.showText({
            'x': item['x']+10,
            'y': item['y']+titleHeight+20,
            'text': item['text'],
            'textsize': item['textsize'],
            'textcolor': item['textcolor'],
            'textalign': item['textalign']
        }, customFont=self.fontText)
        # Buttons
        if item['buttons'] == 2:
            self.showButton({
                    'x': item['x'] + item['width']  - item['buttonwidth'] - 20,
                    'y': item['y'] + item['height'] - item['buttonheight'],
                    'width': item['buttonwidth']+10,
                    'height': item['buttonheight']+10,
                    'color': item['buttoncolor'],
                    'text': item['button2'],
                    'textsize': item['buttonheight'],
                    'textalign': 'center',
                    'textcolor': item['buttontextcolor'],
                    'bordercolor': item['bordercolor'],
                    'border': 1,
            })
            self.showButton({
                    'x': item['x'] + item['width']  - item['buttonwidth']*2 - 40,
                    'y': item['y'] + item['height'] - item['buttonheight'],
                    'width': item['buttonwidth']+10,
                    'height': item['buttonheight']+10,
                    'color': item['buttoncolor'],
                    'text': item['button1'],
                    'textsize': item['buttonheight'],
                    'textalign': 'center',
                    'textcolor': item['buttontextcolor'],
                    'bordercolor': item['bordercolor'],
                    'border': 1,
            })
