# -*- coding: utf-8 -*-
#
# pylint: disable=no-member
# pylint: disable=import-error
#
import os
import sys
import yaml
import pygame
import multiprocessing

import pysplay.const
import pysplay.event
import pysplay.display
import pysplay.touchscreen
import pysplay.utility


# System class with project resources
class system():
    # Class constructor
    def __init__(self, configFile='config.yaml', userObject=None):
        self.__isRunning    = True
        self.__messageQueue = multiprocessing.Queue()
        self.emitterList    = {}
        self.receiverList   = {}
        # Set system properties and normalize self._resources
        self._processTouchEvents = None
        self._path = os.path.dirname(os.path.realpath(configFile))
        self._resourcesLoad(configFile)
        self._resourcesCheck()
        # Initialize user defined object
        self._userObject = userObject(self)
        # Initialize screen
        self._display = pysplay.display(self._resources['screen'][self._currentScreen])
        self.displayShow(self._currentScreen)

    # class destructor
    def __del__(self):
        self.close()

    # Second stage destructor
    def close(self):
        self.__isRunning = False
        # Closing [event queue] process
        if self._processTouchEvents:
            self._processTouchEvents.kill()
            self._processTouchEvents.join()
        # Closing [emitter] processes
        self.emitterClean()

    @property   # Returns program path
    def path(self):
        return self._path

    @property
    def resources(self):
        return self._resources

    @property
    def messageQueue(self):
        return self.__messageQueue

    @property
    def isRunning(self):
        return self.__isRunning

    @property   # Returns currently selected screen
    def screenCurrent(self):
        return self._currentScreen

    @screenCurrent.setter
    def screenCurrent(self, newScreen):
        self._currentScreen = newScreen

    def isScreen(self, screenName):
        if screenName in self._resources['screen']:
            return True
        return False


    # Cleanup emitter/receiver queues on screen change
    def emitterClean(self):
        for emitterName in list(self.emitterList.keys()):
            emitter = self.emitterList[emitterName]
            if emitter:                         # Close forked process with the emitter
                self.emitterList[emitterName].kill()
                self.emitterList[emitterName].join()
            del self.emitterList[emitterName]   # Remove emitter process handle
            del self.receiverList[emitterName]  # Remove receiver function pointer


    # Load display resources from file (YAML)
    def _resourcesLoad(self, configFile):
        with open(self.path + os.sep + configFile) as fileYAML:
            self._resources = yaml.load(fileYAML)


    # All keys to lowercase
    def _resourcesLowercase(self, dictionary):
        for key in dictionary:
            if key != key.lower():
                dictionary[key.lower()] = dictionary[key]
                dictionary.pop(key, None)


    # Scan configuration file and assigns defaults where needed
    def _resourcesCheck(self):
        self._currentScreen = 'main'
        self._resourcesLowercase(self._resources)
        if 'screen' in self._resources:
            # Iterate each screen
            for resource in self._resources['screen']:
                self._resourceCheck(resource)


    # Check [self._resources] to validate and default values when empty
    def _resourceCheck(self, resource):
        self._resourcesLowercase(self._resources['screen'][resource])
        if 'display' not in self._resources['screen'][resource]:    # Display section in [resource] screen is required
            print("ERROR: No 'display' section in screen [{}]".format(resource))
            sys.exit(1)
        self._resourceCheckSetProperties(self._resources['screen'][resource])
        self._resourceCheckSetEvents(self._resources['screen'][resource])
        addResource = []
        for item in self._resources['screen'][resource]['display']:
            self._resourcesLowercase(item)
            # detecting type
            if 'type' not in item: # Unknown item type
                print('ERROR: Item type not found')
                print('    {}'.format(item))
                print('    in screen/{}/display'.format(resource))
                sys.exit(1)
            item['type'] = item['type'].lower()
            # detecting widget
            if item['type']=='box' or item['type']=='button':
                self._resourceCheckSetBoxButton(item)
            elif item['type']=='text':
                self._resourceCheckSetText(item)
            elif item['type']=='windowdialog':
                addResource += self._resourceCheckSetWindowDialog(item)
            elif item['type']=='listbox':
                addResource += self._resourceCheckSetListbox(screen=resource, item=item)
            elif item['type']=='crosshair' or item['type']=='circle':
                self._resourceCheckSetCrosshair(item)
            elif item['type']=='dot':
                self._resourceCheckSetDot(item)
            elif item['type']=='hidden':
                self._resourceCheckSetHidden(item)
            elif item['type']=='image':
                self._resourceCheckSetImage(item)
        # Force a resource rescan [on _resourcesCheck()] on newly added elements
        if len(addResource) > 0:
            self._resources['screen'][resource]['display'] += addResource


    # Detect or set default properties for a specified [resource] screen
    def _resourceCheckSetProperties(self, resource):
        if 'properties' not in resource:
            resource['properties'] = {}
        self._resourceCheckColor(resource['properties'], 'color', '0,0,0')


    # Detect or set default events for a specified [resource] screen
    def _resourceCheckSetEvents(self, resource):
        if 'events' not in resource:
            resource['events'] = {}
        # [open] event
        if 'open' not in resource['events']:
            resource['events']['open'] = None
        else:
            userFunction = resource['events']['open']
            if not userFunction or userFunction=='' or userFunction.lower()=='none':
                resource['events']['open'] = None
        # [close] event
        if 'close' not in resource['events']:
            resource['events']['close'] = None
        else:
            userFunction = resource['events']['close']
            if not userFunction or userFunction=='' or userFunction.lower()=='none':
                resource['events']['close'] = None


    # Default values for widget: [box], [button].  Called from _resourceCheck()
    def _resourceCheckSetBoxButton(self, item):
        # Default color
        self._resourceCheckColor(item, 'color', '0,83,191')
        # Width, Height
        if 'x'      not in item: item['x' ]     = 10
        if 'y'      not in item: item['y' ]     = 10
        if 'width'  not in item: item['width' ] = 100
        if 'height' not in item: item['height'] = 50
        # Touch Coordinates
        self._resourceCheckCoordinate(item, 't_x2', 't_y2', item['x']+item['width'], item['y']+item['height'])
        if item['type']=='button':
            if 'border' not in item: item['border'] = 2
            if 'text' not in item: item['text'] = 'button'
            if 'textsize' not in item: item['textsize'] = 24
            self._resourceCheckAlignment(item, default='center')
            self._resourceCheckColor(item, 'textcolor', '255,255,255')
            self._resourceCheckColor(item, 'bordercolor', '120,120,120')
        else:
            if 'border' not in item: item['border'] = 0
            self._resourceCheckColor(item, 'bordercolor', '255,255,255')
        self._resourceCheckDefault(item)
    # Default values for widget: [text].           Called from _resourceCheck()
    def _resourceCheckSetText(self, item):
        if 'text'      not in item: item['text'] = 'TEXT'
        if 'textsize'  not in item: item['textsize'] = 24
        if 'textfont'  not in item:
            item['textfont'] = 'freesans'
        else:
            item['textfont'] = str(item['textfont'])    # cast it to string
        self._resourceCheckAlignment(item, default='center')
        if 'color' in item:
            item['textcolor'] = item['color']
            item.pop('color', None)
        self._resourceCheckColor(item, 'textcolor', '255,255,255')
        self._resourceCheckDefault(item)
        item.pop('width',  None)
        item.pop('height', None)
    # Default values for widget: [windowdialog].   Called from _resourceCheck()
    def _resourceCheckSetWindowDialog(self, item):
        # Width, Height
        if 'id'           not in item: item['id'] = 'widgetWindowDialog'
        if 'width'        not in item: item['width' ] = 250
        if 'height'       not in item: item['height'] = 100
        if 'buttonwidth'  not in item: item['buttonwidth' ] = 64
        if 'buttonheight' not in item: item['buttonheight'] = 18
        self._resourceCheckColor(item, 'color', '20,20,40')
        self._resourceCheckColor(item, 'bordercolor', '120,120,120')
        self._resourceCheckColor(item, 'buttoncolor', '50,188,228')
        self._resourceCheckColor(item, 'buttontextcolor', '0,0,0')
        # Title and message information
        if 'title'    not in item: item['title']    = 'window title'
        if 'text'     not in item: item['text']     = 'info message'
        if 'textsize' not in item: item['textsize'] = 18
        self._resourceCheckAlignment(item)
        # Button actions
        self._resourceCheckButton(item, 'button1', 'OK')
        self._resourceCheckButton(item, 'button2', 'CANCEL')
        if 'action'  not in item: item['action']  = 'None'
        if 'action2' not in item: item['action2'] = 'None'
        # Create hidden object for these buttons
        item['buttons'] = 0
        resource = []
        if item['button2'] != None:
            item['buttons'] += 1
            newResource = {
                'type': 'hidden',
                'id': item['id']+'button2',
                'x':  item['x'] + item['width']  - item['buttonwidth'] - 20,
                'y':  item['y'] + item['height'] - item['buttonheight'],
                'width':  item['buttonwidth'],
                'height': item['buttonheight'],
                'action': item['action2']
            }
            item['action2'] = None
            self._resourceCheckSetHidden(newResource)
            resource += [newResource]
        if item['button1'] != None:
            item['buttons'] += 1
            newResource = {
                'type': 'hidden',
                'id': item['id']+'button1',
                'x':  item['x'] + item['width']  - item['buttonwidth']*item['buttons'] - 20*item['buttons'],
                'y':  item['y'] + item['height'] - item['buttonheight'],
                'width':  item['buttonwidth'],
                'height': item['buttonheight'],
                'action': item['action']
            }
            item['action'] = None
            self._resourceCheckSetHidden(newResource)
            resource += [newResource]
        self._resourceCheckColor(item, 'textcolor', '255,255,255')
        self._resourceCheckColor(item, 'titlebackground', '20,50,70')
        self._resourceCheckDefault(item)
        return resource
    # Default values for widget: [listbox].        Called from _resourceCheck()
    def _resourceCheckSetListbox(self, screen=None, item=None):
        # Width, Height
        if 'width'  not in item: item['width' ] = 200
        if 'height' not in item: item['height'] = 150
        # widget properties
        if 'id'        not in item: item['id'] = 'listboxWidgetID'
        if 'border'    not in item: item['border'] = 1
        if 'textsize'  not in item: item['textsize'] = 18
        if 'textfont'  not in item:
            item['textfont'] = 'freesans'
        else:
            item['textfont'] = str(item['textfont'])    # cast it to string
        self._resourceCheckAlignment(item)
        self._resourceCheckColor(item, 'color',       '0,0,0')
        self._resourceCheckColor(item, 'textcolor',   '255,255,255')
        self._resourceCheckColor(item, 'bordercolor', '255,255,255')
        if 'scrollbarwidth' not in item: item['scrollbarwidth'] = 40
        item['start'] = 0
        self._resourceCheckDefault(item)
        # Check item['list'] and sanitize it when needed
        item['selected'] = -1
        self.listboxItemsCheck(item)
        # Return calculated resources back to main loop
        item['actionItem'] = item['action']
        item['action'] = None
        return self.__listboxAreaCalculate(screen=screen, item=item)
    
    def listboxItemsCheck(self, listbox):
        if 'list' not in listbox or not listbox['list']:
            listbox['list'] = []
        else:
            for index in range(len(listbox['list'])):
                if listbox['selected'] < 0:
                    listbox['selected'] = index
                # Text
                if isinstance(listbox['list'][index], str) or isinstance(listbox['list'][index], int) or isinstance(listbox['list'][index], float):
                    listbox['list'][index] = {'text': str(listbox['list'][index])}
                elif isinstance(listbox['list'][index], dict):
                    if 'text' not in listbox['list'][index]:
                        listbox['list'][index]['text'] = 'item {}'.format(index)
                else:
                    listbox['list'][index] = {'text': 'item {}'.format(index)}
                # Color
                self._resourceCheckColor(listbox['list'][index], 'color', listbox['textcolor'])
        return listbox

    def listboxRecalcArea(self, screen=None, item=None):
        newResources = self.__listboxAreaCalculate(screen=screen, item=item)
        if len(newResources) > 0:
            self._resources['screen'][screen]['display'] += newResources


    def __listboxAreaCalculate(self, screen=None, item=None):
        # Delete previous hidden areas, if any  
        for widget in list(self._resources['screen'][screen]['display']):
            if 'id' in widget and widget['id'].startswith(item['id']+'_'):
                self._resources['screen'][screen]['display'].remove(widget)
        # count visible items for this list  ([items], [itemsWidth])
        resource = []
        item['pageitems'] = int((item['height']-int(item['textspacing']/2)) / item['textsize'])
        if item['pageitems'] < len(item['list']):
            itemsWidth = item['width']-item['scrollbarwidth']
            # Add scroll bars areas
            newResource = {                 # Scroll UP
                    'type'  : 'hidden',
                    'id'    : item['id']+'_up',
                    'x'     : item['x'] + item['width'] - item['scrollbarwidth'],
                    'y'     : item['y'],
                    'width' : item['scrollbarwidth'],
                    'height': int(item['height']/2),
                    'action': 'listboxScrollUp({screen},{widget})'.format(screen=screen, widget=item['id'])
            }
            self._resourceCheckSetHidden(newResource)
            resource += [newResource]
            newResource = {                 # Scroll DOWN
                    'type'  : 'hidden',
                    'id'    : item['id']+'_down',
                    'x'     : item['x'] + item['width'] - item['scrollbarwidth'],
                    'y'     : item['y'] + int(item['height']/2),
                    'width' : item['scrollbarwidth'],
                    'height': int(item['height']/2),
                    'action': 'listboxScrollDown({screen},{widget})'.format(screen=screen, widget=item['id'])
            }
            self._resourceCheckSetHidden(newResource)
            resource += [newResource]
        else:
            itemsWidth = item['width']

        # Create hidden areas for items onClick() event
        yStart = item['y'] + int(item['textspacing']/2)
        for i in range(item['pageitems']):
            newResource = {
                'type'   : 'hidden',
                'id'     : item['id']+'_'+str(i),
                'x'      : item['x'],
                'y'      : yStart,
                'width'  : itemsWidth,
                'height' : item['textsize'],
                'action' : 'listboxSelect({screen},{widget},{action},{item})'.format(screen=screen, widget=item['id'], action=item['actionItem'], item=i)
            }
            yStart += item['textsize']
            self._resourceCheckSetHidden(newResource)
            resource += [newResource]
        return resource

    # Default values for widget: [crosshair].      Called from _resourceCheck()
    def _resourceCheckSetCrosshair(self, item):
        if 'x'      not in item: item['x'] = 10
        if 'y'      not in item: item['y'] = 10
        if 'fill'   not in item: item['fill'] = 'false'
        if str(item['fill']).lower() in ['true', '1', 't', 'y', 'yes']:
            item['fill'] = True
        else:
            item['fill'] = False
        if 'radius' not in item: item['radius'] = 10
        # Touch Coordinates
        self._resourceCheckCoordinate(item, 't_x1', 't_y1', item['x']-item['radius'], item['y']-item['radius'])
        self._resourceCheckCoordinate(item, 't_x2', 't_y2', item['x']+item['radius'], item['y']+item['radius'])
        # Apply default values
        self._resourceCheckDefault(item)
    # Default values for widget: [dot].            Called from _resourceCheck()
    def _resourceCheckSetDot(self, item):
        if 'x' not in item: item['x'] = 100
        if 'y' not in item: item['y'] = 100
        self._resourceCheckDefault(item)
    # Defatul values for widget: [hidden].         Called from _resourceCheck()
    def _resourceCheckSetHidden(self, item):
        if 'width'  not in item: item['width' ] = 64
        if 'height' not in item: item['height'] = 18
        self._resourceCheckCoordinate(item, 't_x2', 't_y2', item['x']+item['width'], item['y']+item['height'])
        self._resourceCheckDefault(item)
        item.pop('color', None)
    # Default values for widget: [image]
    def _resourceCheckSetImage(self, item):
        if 'x'   not in item: item['x'] = 10
        if 'y'   not in item: item['y'] = 10
        if 'src' not in item:
            sys.exit("type: image, missing [src] attribute")
        item['src'] = os.path.join(self._path, item['src'])
        if not os.path.exists(item['src']):
            sys.exit("type: image, file '{}' does not exists".format(item['src']))
        image = pygame.image.load(item['src'])
        self._resourceCheckCoordinate(item, 't_x2', 't_y2', item['x']+image.get_width(), item['y']+image.get_height())
        self._resourceCheckDefault(item)
        item.pop('color', None)

    # Set default properties for a widget
    def _resourceCheckDefault(self, item):
        if 'id'     not in item: item['id']     = 'widgetID'
        if 'x'      not in item: item['x']      = 10
        if 'y'      not in item: item['y']      = 10
        if 'action' not in item: item['action'] = 'None'
        # Assign default color
        self._resourceCheckColor(item, 'color', '255,255,255')
        # Touch Coordinates
        self._resourceCheckCoordinate(item, 't_x1', 't_y1', item['x'], item['y'])
        self._resourceCheckCoordinate(item, 't_x2', 't_y2', item['x'], item['y'])
        self._resourceCheckCoordinateOrder(item)
    # Set default alignment for the widget
    def _resourceCheckAlignment(self, item, default='left'):
        item['textalign'] = default if 'textalign' not in item else item['textalign'].lower()
        if item['textalign'] not in ['left', 'center', 'right']:
            item['textalign'] = default
        item['textspacing'] = 10 if 'textspacing' not in item else int(item['textspacing'])+0
    # Assign a label to a Button
    def _resourceCheckButton(self, item, buttonName, defaultValue):
        item[buttonName] = defaultValue if buttonName not in item else item[buttonName]
        if item[buttonName].lower() == 'none':
            item[buttonName] = None
        if ((item[buttonName].startswith('"') and item[buttonName].endswith('"')) or
            (item[buttonName].startswith("'") and item[buttonName].endswith("'")) ):
                item[buttonName] = item[buttonName][1:-1]
    # Translate virtual coordinates to physical ones
    def _resourceCheckCoordinate(self, item, nameTouchX, nameTouchY, valueX, valueY):
        (touchXvalue, touchYvalue) = pysplay.const.coordToTouch(valueX, valueY)
        if nameTouchX not in item:
            item[nameTouchX] = touchXvalue
        if nameTouchY not in item:
            item[nameTouchY] = touchYvalue
    # Set coords to always have: (t_x1<t_x2, t_y1<t_y2)
    def _resourceCheckCoordinateOrder(self, item):
        if item['t_x1'] > item['t_x2']:
            value        = item['t_x2']
            item['t_x2'] = item['t_x1']
            item['t_x1'] = value
        if item['t_y1'] > item['t_y2']:
            value        = item['t_y2']
            item['t_y2'] = item['t_y1']
            item['t_y1'] = value
    # Detect color properties and assign default if not present
    def _resourceCheckColor(self, item, colorname, default):
        if colorname not in item:
            item[colorname] = default
        # (tuple) -> string
        if type(item[colorname])==tuple:
            item[colorname] = ','.join(map(str, item[colorname]))
        # String -> (tuple)
        item[colorname] = tuple(map(int, item[colorname].replace(' ','').split(',')))

    # Display a "please wait" screen
    def displayWait(self, text):
        self._display.wait(text)

    # Display selected [screenName]
    def displayShow(self, screenName):
        self._display.clear()
        self.displayPopup(screenName)

    # Close selected [screenName]
    def displayClose(self, screenName):
        self.__displayEvent(screenName=screenName, eventName='close')

    # Display selected [screenName] without clearing the page (popup mode)
    def displayPopup(self, screenName):
        self.__displayEvent(screenName=screenName, eventName='open')    # Fire 'open' event before the page is shown
        self._display.show(self._resources['screen'][screenName])       # Display screen

    # Run [events/(eventName)] action
    def __displayEvent(self, screenName=None, eventName=None):
        functionName = self._resources['screen'][screenName]['events'][eventName]
        if functionName:                # check if there's a function binded to this event or a generic [None]
            eventAction = pysplay.utility.functionGet(functionName)
            if eventAction:             # check if this is a valid function with a string parser
                try:
                    pysplay.utility.functionExecute(self._userObject, *eventAction)
                except Exception as E:
                    print("\nERROR: Cannot execute [{}] method '{}' for screen '{}'.".format(eventName, functionName, screenName))


    # Test/Debug features, useful for screen calibration
    def calibration(self):
        # Force rewrite main screen with Calibration Screen [SCREEN_CALIBRATION]
        self._resources['screen'][self._currentScreen] = pysplay.const.SCREEN_CALIBRATION
        self._resourceCheck(self._currentScreen)
        self.displayShow(self._currentScreen)
        points = []
        pysplay.const.getCoord = lambda a,b: (a, b)         # Redefining lambda to keep plain values without transformations
        print("\n\nFollow the blue crosshair, press <ENTER> to confirm")
        print("1> ", end='', flush=True)
        # Forking multiprocess queue to get events from there
        self._processTouchEvents = multiprocessing.Process(target=pysplay.eventProcess, args=(self.__messageQueue,))
        self._processTouchEvents.start()
        while self.__isRunning:
            message = self.__messageQueue.get()
            try:
                if message['type'] == 'event':
                    (X, Y) = message['data']
                    if X:
                        confirm = input("A={:<6} B={:<6}   Confirm [n|Y] ? ".format(X, Y)).lower()
                        if confirm=='' or confirm=='y':
                            points.append((X,Y))
                        if len(points) < 5:
                            self._resources['screen'][self._currentScreen]['display'][len(points)-1].update({'fill':True, 'color':'255,255,255'})
                            self._resources['screen'][self._currentScreen]['display'][len(points)].update({'color':'0,0,255'})
                            self._resourceCheck(self._currentScreen)
                            self.displayShow(self._currentScreen)
                        else:
                            print("   {}\n".format(points))
                            self.close()
                            break
                        print("{}> ".format(len(points)+1), end='', flush=True)
            except Exception as E:
                errorFile, errorLine, errorType = pysplay.utility.getError()
                print('\nERROR: {}'.format(E))
                print('       {}:{},  {}'.format(errorFile, errorLine, errorType))

    # Main event loop
    def loop(self):
        self._processTouchEvents = multiprocessing.Process(target=pysplay.eventProcess, args=(self.__messageQueue,))
        self._processTouchEvents.start()
        while self.__isRunning:
            message = self.__messageQueue.get()
            try:
                if message['type'] == 'event':
                    (X, Y) = message['data']
                    if X:
                        self._widgetDetect(X, Y)
                elif message['type'] == 'emitter':
                    emitterFunction = self.receiverList[message['emitter']]
                    emitterFunction(message['data'])

            except Exception as E:
                errorFile, errorLine, errorType = pysplay.utility.getError()
                print('\nERROR: {}'.format(E))
                print('       {}:{},  {}'.format(errorFile, errorLine, errorType))
                print('       Msg={}'.format(message))

    # Detect possible selected widget on touch event, if any. Called by [self.loop()]
    def _widgetDetect(self, X, Y):
        for widget in self._resources['screen'][self._currentScreen]['display']:
            if widget['t_x1'] < X and X < widget['t_x2'] and widget['t_y1'] < Y and Y < widget['t_y2']:
                userAction = pysplay.utility.functionGet(widget['action'])
                if userAction:  # Execute user defined action
                    try:
                        pysplay.utility.functionExecute(self._userObject, *userAction)
                    except:
                        pass

    # Get widget from screen
    def widgetGet(self, screenName, widgetID):
        for item in self._resources['screen'][screenName]['display']:
            if item['id'] == widgetID:
                return item
        return None

    # Get a specific widget property from screen
    def widgetGetKey(self, screenName, widgetID, key):
        for item in self._resources['screen'][screenName]['display']:
            if item['id'] == widgetID:
                return item[key]
        return None

    # Edit a specific widget property inside a display
    def widgetSetKey(self, screenName, widgetID, key, value):
        for item in self._resources['screen'][screenName]['display']:
            if item['id'] == widgetID:
                item[key] = value
    
    # Draw a widget
    def widgetShow(self, widget=None, refresh=True):
        if widget:
            self._display.widgetShow(widget, refresh)

    # Refresh a widget, clear old widget and draw a new one
    def widgetRefresh(self, widgetOld=None, widgetNew=None, refresh=True):
        self._display.widgetRefresh(widgetOld=widgetOld, widgetNew=widgetNew, refresh=refresh)

    # Returns selected screen properties
    def screenProperty(self, screenName):
        return self._resources['screen'][screenName]['properties']

    # Set a specific screen property
    def screenPropertySet(self, screenName=None, key=None, value=None):
        self._resources['screen'][screenName]['properties'][key] = value
