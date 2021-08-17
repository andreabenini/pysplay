# -*- coding: utf-8 -*-
#
# Package common utilities.
# Cluster of useful function for the entire package
# 
#
# pylint: disable=no-member
# pylint: disable=import-error
#
import re
import os
import sys
import time
from csv import reader
from datetime import datetime


def functionGet(actionString):
    if not actionString or actionString == '' or actionString.lower() == 'none':
        return None
    action  = tuple()
    # Function Name
    functionName = re.findall(r"(?P<function>[a-zA-Z]*).*", actionString)
    if functionName:
        action += (functionName[0], )
    # Parameters, if any
    parameters = re.findall(r".*\((?P<params>.*)\)", actionString)
    if parameters:
        # Get list of parameters in (paramList)
        paramList = []
        for item in reader([parameters[0]], delimiter=',', quotechar="'"):
            paramList += item
        # strip leading/trailing "' and add [item] to [action] tuple
        for item in paramList:
            item = item.strip()
            if (item.startswith('"') and item.endswith('"')) or (item.startswith("'") and item.endswith("'")):
                item = item[1:-1]
            if item and item!='':
                action += (item,)
    return action


# Execute an user's object function. System class calls it to eval user's code
def functionExecute(userObject, name: str, *args, **kwargs):
    if hasattr(userObject, name):
        userFunction = getattr(userObject, name)
        if callable(userFunction):
            userFunction(*args)
            return
    print(f"Cannot execute user defined method:  {object.__class__.__name__}->{name}()")


# @return errorFile, errorLine, errorType (tuple)
def getError():
    errorType, _, exc_tb = sys.exc_info()
    errorFile = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    return errorFile, exc_tb.tb_lineno, errorType


# bytes to pretty format string
#    1000 -> "1 Kb"
#   10000 -> "10 Kb"
# 1000000 -> "1 Mb"
# ...
def bytePrettyStr(num):
    for unit in ['','Kb','Mb','Gb','Tb','Pb','Eb','Zb']:
        if abs(num) < 1024.0:
            return "{:3.1f} {}".format(num, unit)
        num /= 1024.0
    return "{:.1f} {}".format(num, 'Yb')


# Cast to int [Whatever] or return [defaultOnError] on error
def toInt(Whatever, defaultOnError):
    try:
        return int(Whatever)
    except ValueError:
        return defaultOnError

# python datetime to pretty string (YYYY/MM/DD HH:MM:SS)
def datetimeToStr(now=None, format='%Y/%m/%d %H:%M:%S'):
    if not now:
        now = datetime.now()
    return now.strftime(format)

# UNIX time to pretty string (YYYY/MM/DD HH:MM:SS)
def unixdatetimeToStr(ts=None, format='%Y/%m/%d %H:%M:%S'):
    if not ts:
        ts = time.time()
    else:
        ts = float(ts)
    return datetime.utcfromtimestamp(ts).strftime(format)

# Seconds to human readable string format (example: 3600 -> '1h')
def secondsToDaysHoursMinutesStr(time=None):
    if not time:
        return ''
    if isinstance(time, str) and not time.isdigit():
        return ''
    time = int(float(time))
    result = ''
    day  = int(time // (24 * 3600))
    time = time % (24 * 3600)
    hour = int(time // 3600)
    time %= 3600
    minutes = int(time // 60)
    if day > 0:
        result = '{:d} d, '.format(day)
    if hour > 0:
        result += '{:d} h, '.format(hour)
    if minutes > 0:
        result += '{:d} min'.format(minutes)
    return result

