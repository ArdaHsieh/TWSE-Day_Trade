#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Screen Stocks
Type: Tool
Auther: Arda
"""
# Public modules
import requests
import datetime
import time


# Get html content
class htmlgetter(object):
    # Request web page with url and method get.
    def geturl(self, url):
        headers = {
                   'user-agent': 'Mozilla/5.0 (Windows NT 6.1)'
                               + 'AppleWebKit/537.36 (KHTML, like Gecko)'
                               + 'Chrome/52.0.2743.116 Safari/537.36'
                  }
        
        return requests.get(url, headers = headers).text#.encode('utf-8-sig')
    
    
# Time transfer tools.
class timetrans:
    # Get timestamp from date.
    def timestamp(self, date):
        datetime8 = date + '08'
        return time.mktime(datetime.datetime.strptime(datetime8, "%Y%m%d%H").timetuple())
    

# Number tools.
class numtrans:
    # convert number strings to number.
    #for example, 1,900 to 1900.
    def strtonum(self, string):
        num = ''
        for char in string:
            if char in ['-', '.', '0', '1', '2', '3' , '4', '5', '6', '7', '8', '9']:
                num += char
        return float(num)