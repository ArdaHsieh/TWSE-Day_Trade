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

        return [1 + sum(UpMA)/(2*(sum(UpMA)+sum(DownMA))),
                1 + sum(DownMA)/(2*(sum(UpMA)+sum(DownMA)))]
            

    # Return Bollinger Bands' top and buttom which are amplitude/10 + 1.5
    # and Bollinger Bands' wide
    # Return float.
    def bbandsparm(self, stockNum, stockAmp, date):
        dateTS = '[' + str(int((bcmethod.timetrans().timestamp(date)))) + '000'
        url = ( 'https://www.wantgoo.com/stock/'
              + '%E5%80%8B%E8%82%A1%E7%B7%9A%E5%9C%96/%E6%8A%80%E8%A1%93%E7%B7%9A%E5%9C%96%E8%B3%87%E6%96%99?'
              + 'StockNo=' + stockNum + '&Kcounts=484&Type=%E6%97%A5K_%E6%94%B6%E7%9B%A4%E5%83%B9&isCleanCache=false')
        priceMAText = json.loads(bcmethod.htmlgetter().geturl(url))['returnValues']['value']
        PriceMA = priceMAText.split(',')
        PriceMA = PriceMA[::-1]
        
        for i in range(len(PriceMA)):
            if PriceMA[i] == dateTS:
                priceAvg = float(PriceMA[i-1][0:-2])
                break
            
        return [float(stockAmp)/10.0 + 1.5, priceAvg*0.015]