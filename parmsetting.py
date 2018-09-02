#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TWSE parameter getter.
Type: class, Tool
Auther: Arda
"""
# Public modules
import json
from bs4 import BeautifulSoup
import datetime
import time
import numpy as np

# My modules
import basiccrawlmethod as bcmethod


class getparm:    
    # return MA top and buttom %.
    def maparm(self, stockNum, date):
        dateText = date[0:4] + '/' + date[4:6] + '/' + date[6:8]
        url = 'https://www.wantgoo.com/stock/astock/agentstat2?stockno=' + stockNum
        maData = bcmethod.htmlgetter().geturl(url)
        soup = BeautifulSoup(maData, 'html.parser')
        MAData = soup.find_all('table', {'id':'listResult'})
        MAData = MAData[0].find_all('tbody')
        MAData = MAData[0].find_all('tr')
        
        for i in range(len(MAData)):
            Data = MAData[i].find_all('td')
            if Data[0].text == dateText:
                start = i
        
        UpMA, DownMA = [], []
        
        for i in range(5):
            Data = MAData[start + i].find_all('td')
            if Data[1].text[0] == '-':
                num = bcmethod.numtrans().strtonum(Data[1].text)
                DownMA.append(abs(num))
            else:
                num = bcmethod.numtrans().strtonum(Data[1].text)
                UpMA.append(num)

        if len(UpMA) and len(DownMA):
            return (1 + sum(UpMA)/(2*(sum(UpMA)+sum(DownMA))),
                    1 + sum(DownMA)/(2*(sum(UpMA)+sum(DownMA))))
        else:
            url = ('https://www.wantgoo.com/stock/astock/agentstat_total_ajax?StockNo='
                  + stockNum + '&StartDate=' + date + '&EndDate=' + date)
            maData = bcmethod.htmlgetter().geturl(url)
            maDataText = json.loads(bcmethod.htmlgetter().geturl(url))['returnValues']
            MAData = maDataText.split(',')
            up = bcmethod.numtrans().strtonum(MAData[0])
            dn = abs(bcmethod.numtrans().strtonum(MAData[1]))

            if len(UpMA):
                return 1 + up/(2*(up+dn)), 1 + dn/(2*(up+dn))
            elif len(DownMA):
                return 1 + dn/(2*(up+dn)), 1 + up/(2*(up+dn))       