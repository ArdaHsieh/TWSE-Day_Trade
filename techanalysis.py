#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TWSE technical analysis.
Type: class, Tool
Auther: Arda
"""
# Public modules
import json

# My modules
import basiccrawlmethod as bcmethod


class techmethod:
    # RSI (Relative Strength Index)
    # Call rsi as rsi(stock number, date, days) => rsi(str, str, int)
    # for example rsi('0050', '20180830', 5)
    # date = yyyymmdd
    # Return a float, for example, 65.5 means RSI = 65.5% .
    def rsi(self, stockNum, date, days=5):
        dateTS = int((bcmethod.timetrans().timestamp(date)))*1000
        url = ( 'https://www.wantgoo.com/stock/techchart/highchartdata?'
              + 'StockNo=' + stockNum 
              + '&Kcounts=10&Type=%E6%97%A5K_RSI%7C' )
        
        rsiDataText = json.loads(bcmethod.htmlgetter().geturl(url))['returnValues']['value']  
        data = rsiDataText.split('=')

        RsiData = eval(data[int(days/5)].split(';')[0])
        
        for i in range(len(RsiData)):
            if dateTS == RsiData[i]['x']:
                return RsiData[i]['y']
                break
    
    
    # MA (Moving Average)
    # Call ma as ma(stock number, date, days) => rsi(str, str, int)
    # days = 5, 10, 20, 60, 120
    # for example ma('0050', '20180830', 5)
    # date = yyyymmdd
    # Return a float.
    def ma(self, stockNum, date, days=20):
        Days = [5, 10, 20, 60, 120]
        dateTS = int((bcmethod.timetrans().timestamp(date)))*1000
        url = ( 'https://www.wantgoo.com/stock/techchart/highchartdata?'
              + 'StockNo=' + stockNum 
              + '&Kcounts=10&Type=日K_K線%7C日' )
        
        maDataText = json.loads(bcmethod.htmlgetter().geturl(url))['returnValues']['value']
        data = maDataText.split('=')
        
        i = Days.index(days) + 3
        MaData = eval(data[i].split(';')[0])
        
        for j in range(len(MaData)):
            if dateTS == MaData[j]['x']:
                return MaData[j]['y']
                break                    