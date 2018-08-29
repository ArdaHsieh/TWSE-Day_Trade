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
import numpy as np


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
    
    
    # RSI (Relative Strength Index)
    # Call rsi as rsi(stock number, days, date) => rsi(str, int, str)
    # for example rsi('0050', 5, '20180830')
    # date = yyyymmdd
    # Return a float, for example, 65.5 means RSI = 65.5% .
    def rsi(self, stocknum, days, date):
        # Get last month and last last month.
        if int(date[6:8]) > 15:
            pre1 = str(datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:8])) 
                      - datetime.timedelta(days=31))
        else:
            pre1 = str(datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:8])) 
                      - datetime.timedelta(days=15))
        pre1 = pre1.split('-')
        pre1month = pre1[0] + pre1[1] + pre1[2]
        
        
        if int(date[6:8]) > 15:
            pre2 = str(datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:8])) 
                      - datetime.timedelta(days=62))
        else:
            pre2 = str(datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:8])) 
                      - datetime.timedelta(days=46))
        pre2 = pre2.split('-')
        pre2month = pre2[0] + pre2[1] + pre2[2]
        
        # Get data              
        urlTWSE = "http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=" + pre2month + "&stockNo=" + stocknum
        RSIBData2 = json.loads(self.geturl(urlTWSE))['data']
        
        urlTWSE = "http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=" + pre1month + "&stockNo=" + stocknum
        RSIBData1 = json.loads(self.geturl(urlTWSE))['data']
        
        urlTWSE = "http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=" + date + "&stockNo=" + stocknum
        RSIBData0= json.loads(self.geturl(urlTWSE))['data']
        
        RSIBData = np.append(RSIBData2, RSIBData1, axis=0)
        RSIBData = np.append(RSIBData, RSIBData0, axis=0)
        RSIBData = RSIBData[::-1]
        
        # Get start index
        date = str(int(date[0:4])-1911) + '/' + date[4:6] + '/' + date[6:8]
        for i in range(len(RSIBData)):
            if date == RSIBData[i][0]:
                startindex = i
                break
        
        # Calculate RSI
        up = 0.0
        down = 0.0
        for i in range(startindex, startindex+int(days)):
            if RSIBData[i][-2][0] == '+':
                up += float(RSIBData[i][-2][1::])
            elif RSIBData[i][-2][0] == '-':
                down = float(RSIBData[i][-2][1::])
        
        return (100.0 * up) / (up + down)