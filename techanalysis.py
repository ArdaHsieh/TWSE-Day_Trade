#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TWSE technical analysis.
Type: class, Tool
Auther: Arda
"""

import requests
import json
from bs4 import BeautifulSoup
import datetime


class techmethod:
    # Request web page with url and the method GET.
    # Is an inside class function.
    def geturl(self, url):
        headers = {
                   'user-agent': 'Mozilla/5.0 (Windows NT 6.1)'
                               + 'AppleWebKit/537.36 (KHTML, like Gecko)'
                               + 'Chrome/52.0.2743.116 Safari/537.36'
                  }
    
        return requests.get(url, headers = headers).text.encode('utf-8-sig')
    
    
    # RSI
    # Call rsi as rsi(stock number, days, date) => rsi(str, int, str)
    # for example rsi('0050', 5, '20180830')
    # date = yyyymmdd
    # Return a float as %2f for example 0.65 means RSI = 65% .
    def rsi(stocknum, days, date):