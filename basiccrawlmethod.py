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
class htmlgetter:
    # Request web page with url and method get.
    def geturl(url):
        headers = {
                   'user-agent': 'Mozilla/5.0 (Windows NT 6.1)'
                               + 'AppleWebKit/537.36 (KHTML, like Gecko)'
                               + 'Chrome/52.0.2743.116 Safari/537.36'
                  }   
        return requests.get(url, headers = headers).text.encode('utf-8-sig')
    
    
# Get timestamp.
class timetrans:
    def timestamp(self, date):
        datetime8 = date + '08'
        return time.mktime(datetime.datetime.strptime(datetime8, "%Y%m%d%H").timetuple())