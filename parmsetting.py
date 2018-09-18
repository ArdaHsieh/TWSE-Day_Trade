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
    def bbandsparm(self, stockNum, stockAmp, closeDay):
        urlTWSE = ( "http://www.tse.com.tw/exchangeReport/STOCK_DAY?response=json&date="
                  + closeDay + "&stockNo=" + stockNum)
        StockTradeData = json.loads(bcmethod.htmlgetter().geturl(urlTWSE))['data']       
        for stock in StockTradeData:
            if bcmethod.timetrans().ad2re(closeDay) in stock:
                vol = bcmethod.numtrans().strtonum(stock[1])
                val = bcmethod.numtrans().strtonum(stock[2])
                meanPrice = (val / vol)
                break
        return [meanPrice, float(stockAmp)/10.0 + 1.5, meanPrice*0.015]