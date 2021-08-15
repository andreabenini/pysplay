# -*- coding: utf-8 -*-
#
# pylint: disable=no-member
# pylint: disable=import-error
#
import os
from re import S
import requests
import multiprocessing
import pysplay.utility


# Emitter message class
class emitterMessage():
    def __init__(self, queue, emitter):
        self.__msg = {'type': 'emitter', 'emitter': emitter, 'data': None}
        self.__queue = queue
    def send(self, message):
        self.__msg['data'] = message
        self.__queue.put(self.__msg)


# User's class
class userobject():
    def __init__(self, system):
        self.__previousScreen = ''
        self.__system = system

    @property
    def screenCurrent(self):
        return self.__system.screenCurrent
    @screenCurrent.setter
    def screenCurrent(self, newScreen):
        self.__system.screenCurrent = newScreen

    @property
    def resource(self):
        return self.__system.resources

    @property
    def isRunning(self):
        return self.__system.isRunning

    def systemExit(self):
        self.__system.displayWait("...wait...")
        self.__system.close()
    
    def systemReboot(self):
        self.__system.displayWait("...wait...")
        os.system('sudo reboot')

    def systemShutdown(self):
        self.__system.displayWait("...wait...")
        os.system('sudo poweroff')

    def test(self):
        print("test() function, nothing special here...")

    def testListbox(self, listbox, index):
        print('testListbox() function selected')
        print('            ID   = {}'.format(listbox['id']))
        print('            Item = {}'.format(listbox['list'][index]['text']))


    # HTTP 'GET' request
    def httpGet(self, url=None, headers=None):
        if not url:
            return None
        return requests.get(url, headers=headers)
    # HTTP 'DELETE' request
    def httpDelete(self, url=None, headers=None):
        if not url:
            return None
        return requests.delete(url, headers=headers)
    # HTTP 'POST' request
    def httpPost(self, url=None, headers=None, jsonPayload=None):
        if not url:
            return None
        return requests.post(url, headers=headers, json=jsonPayload)


    # Close current screen and return to previous one, useful with confirm() method
    def close(self):
        self.screenCurrent = self.__previousScreen
        self.__system.displayShow(self.screenCurrent)

    # Get listbox widget
    def listboxGet(self, screen=None, widget=None):
        if not screen or not widget:
            return None
        return self.__system.widgetGet(screen, widget)

    # Listbox, Clear items list
    # @param screen   (string) Screen name [mandatory]
    # @param widget   (string) Listbox widget name [mandatory]
    # @param show    (boolean) Redraw widget after cleanup
    #
    # @return listbox (widget) 
    # @return None             on error
    def listboxClear(self, screen=None, widget=None, show=False):
        listbox = self.listboxGet(widget=widget, screen=screen)
        if not listbox:
            return None
        listbox['list'] = []
        listbox['selected'] = -1
        if show:
            self.listboxShow(screen=screen, widget=widget, listbox=listbox)
        return listbox

    # @param screen  (string) [optional] Screen name
    # @param widget  (string) [optional] Listbox widget name
    # @param listbox (object) [optional] Listbox widget name
    # @param show    (boolean) Redraw widget after adding item
    #
    # @return listbox (widget) 
    #
    # @see [screen] and [widget] are required when [listbox] is None
    #      [listbox] is required when [screen] and [widget] are None
    def listboxItemAdd(self, screen=None, widget=None, listbox=None, item=None, show=False):
        if not item:
            return None
        if not listbox:
            listbox = self.listboxGet(screen=screen, widget=widget)
            if not listbox:
                return None
        if isinstance(item, str) or isinstance(item, int) or isinstance(item, float):
            listbox['list'] += [str(item)]
        else:
            listbox['list'] += [item]
        self.__system.listboxItemsCheck(listbox)
        if show:
            self.listboxShow(screen=screen, widget=widget, listbox=listbox)
        return listbox

    def listboxItemSelected(self, screen=None, widget=None):
        listbox = self.listboxGet(screen=screen, widget=widget)
        if not listbox or listbox['selected']<0:
            return None
        return listbox['list'][listbox['selected']]

    # @param widget (object) widget to redraw (from listboxClear(),listboxItemAdd())
    #
    # @see [screen] and [widget] are mandatory
    def listboxShow(self, screen=None, widget=None, listbox=None):
        if not listbox:
            listbox = self.listboxGet(screen=screen, widget=widget)
            if not listbox:
                return None
        elif not screen:
            return None
        if listbox['selected'] == -1:
            listbox['selected'] = listbox['start']
        self.__system.listboxRecalcArea(screen=screen, item=listbox)
        self.__system.widgetShow(listbox)

    # Sort internal listbox['list'] items alphabetically
    def listboxSort(self, listbox=None, sortAscending=True, ignoreCase=False):
        if not listbox:
            return
        if ignoreCase:
            listbox['list'] = sorted(listbox['list'], key=lambda k: k['text'].lower(), reverse=(not sortAscending))
        else:
            listbox['list'] = sorted(listbox['list'], key=lambda k: k['text'],         reverse=(not sortAscending))

    # Listbox, Select item and execute user function
    # @param screen (string)  Screen name (from screen resources)
    # @param widget (string)  Widget['id'] Name (inside [screen])
    # @param action (string)  Action to execute. User defined function to execute
    # @param item   (integer) listbox item selected
    def listboxSelect(self, screen=None, widget=None, action=None, item=0):
        listbox = self.listboxGet(screen=screen, widget=widget)
        if not listbox:
            return
        index = listbox['start']+int(item)
        if index >= len(listbox['list']):
            return
        listbox['selected'] = index
        pysplay.utility.functionExecute(self, action, listbox, index)

    # Listbox, Page UP
    def listboxScrollUp(self, screen=None, widget=None):
        listbox = self.listboxGet(screen=screen, widget=widget)
        if not listbox:
            return
        start = int(listbox['start']) - int(listbox['pageitems'])
        if start < 0:
            start = 0
        self.__system.widgetSetKey(screen, widget, 'start', start)
        self.__system.widgetShow(listbox)

    # Listbox, Page Down
    def listboxScrollDown(self, screen=None, widget=None):
        listbox = self.listboxGet(screen=screen, widget=widget)
        if not listbox:
            return
        start = int(listbox['start']) + int(listbox['pageitems'])
        if start >= len(listbox['list']):
            start = len(listbox['list']) - int(listbox['pageitems'])
        if start < 0:
            start = 0
        self.__system.widgetSetKey(screen, widget, 'start', start)
        self.__system.widgetShow(listbox)

    # Dispaly a new text in a [text] widget item
    def textShow(self, screenName=None, widgetName=None, textValue=None, show=True):
        if not screenName or not widgetName or not textValue:
            return
        widget = self.__system.widgetGet(screenName, widgetName)
        if not widget:
            return
        previousText = widget.copy()
        previousText['textcolor'] = self.__system.screenProperty(screenName)['color']
        widget['text'] = textValue
        self.__system.widgetRefresh(widgetOld=previousText, widgetNew=widget, refresh=show)


    def widgetSet(self, screenName=None, widgetName=None, key=None, value=None):
        self.__system.widgetSetKey(screenName, widgetName, key, value)

    def widgetShow(self, screenName=None, widgetName=None, refresh=True):
        widget = self.__system.widgetGet(screenName, widgetName)
        self.__system.widgetShow(widget=widget, refresh=refresh)


    def screenPropertySet(self, screenName=None, key=None, value=None):
        self.__system.screenPropertySet(screenName=screenName, key=key, value=value)

    def screenPropertyGet(self, screenName=None, key=None):
        return self.__system.screenProperty(screenName=screenName)[key]


    # Open a confirm box (YES|NO|CANCEL, OK|Cancel, ...)
    def confirm(self, screenConfirm=None, dialogWidget=None, title='confirm', message='Are you sure ?', action1='close()', action2='close()'):
        if not screenConfirm or not dialogWidget:
            return
        self.__previousScreen = self.screenCurrent
        self.screenCurrent   = screenConfirm
        self.__system.widgetSetKey(screenConfirm, dialogWidget, 'title',   title)
        self.__system.widgetSetKey(screenConfirm, dialogWidget, 'text',    message)
        if action1.lower() != 'none':
            self.__system.widgetSetKey(screenConfirm, dialogWidget+'button1', 'action', action1)
        if action2.lower() != 'none':
            self.__system.widgetSetKey(screenConfirm, dialogWidget+'button2', 'action', action2)
        self.__system.displayPopup(screenConfirm)

    # Goto a menu [menuName]
    def menu(self, menuName):
        if not self.__system.isScreen(menuName):
            return
        self.__system.displayClose(self.screenCurrent)
        self.__system.emitterClean()
        self.screenCurrent = menuName
        self.__system.displayShow(menuName)


    # Define an emitter on screen
    def emitter(self, emitterFunction=None, receiverFunction=None):
        if emitterFunction:
            functionExecute  = pysplay.utility.functionGet(emitterFunction)
            functionReceiver = getattr(self, receiverFunction) if hasattr(self, receiverFunction) else None
            if functionExecute and functionReceiver:
                self.__system.emitterList[emitterFunction] = multiprocessing.Process(target=self.__emitterStarter, args=(self.__system.messageQueue, emitterFunction, functionExecute,))
                self.__system.emitterList[emitterFunction].start()
                self.__system.receiverList[emitterFunction] = functionReceiver
                return True
        return False
    # Start an emitter, called by [emitter()]
    def __emitterStarter(self, messageQueue, emitterFunction, functionExecute):
        message = emitterMessage(messageQueue, emitterFunction)
        functionExecute += (message,)       # Add message queue to function executor
        try: pysplay.utility.functionExecute(self, *functionExecute)
        except: pass
