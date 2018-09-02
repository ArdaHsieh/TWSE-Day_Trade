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
import basiccarwlmethod as bcmethod


class techmethod:
    # RSI (Relative Strength Index)
    # Call rsi as rsi(stock number, date, days) => rsi(str, str, int)
    # for example rsi('0050', '20180830', 5)
    # date = yyyymmdd
    # Return a float, for example, 65.5 means RSI = 65.5% .
    def rsi(self, stocknum, date, days=5):
        dateTS = '[' + str(int((bcmethod.timetrans().timestamp(date)))) + '000'
        url = ( 'https://www.wantgoo.com/stock/' 
              + '%E5%80%8B%E8%82%A1%E7%B7%9A%E5%9C%96/%E6%8A%80%E8%A1%93%E7%B7%9A%E5%9C%96%E8%B3%87%E6%96%99?'
              + 'StockNo=' + stocknum 
              + '&Kcounts=245&Type=%E6%97%A5K_RSI&isCleanCache=false')
        
        rsiDataText = json.loads(bcmethod.htmlgetter().geturl(url))['returnValues']['value']
        data = rsiDataText.split('=')

        rsiData = data[int(days/5)].split(';')
        RsiData = rsiData[0].split(',')
        RsiData = RsiData[::-1]
        
        for i in range(len(RsiData)):
            if RsiData[i] == dateTS:
                return float(RsiData[i-1][0:-2])
                break
    
    
    # MA (Relative Strength Index)
    # Call ma as ma(stock number, date, days) => rsi(str, str, int)
    # days = 5, 10, 20, 60, 120
    # for example ma('0050', '20180830', 5)
    # date = yyyymmdd
    # Return a float.
    def ma(self, stocknum, date, days=20):
        Days = [5, 10, 20, 60, 120]
        dateTS = '[' + str(int((bcmethod.timetrans().timestamp(date)))) + '000'
        url = ( 'https://www.wantgoo.com/stock/'
              + '%E5%80%8B%E8%82%A1%E7%B7%9A%E5%9C%96/%E6%8A%80%E8%A1%93%E7%B7%9A%E5%9C%96%E8%B3%87%E6%96%99?'
              + 'StockNo=' + stocknum
              + '&Kcounts=120&Type=%E6%97%A5K_K%E7%B7%9A%7C%E6%97%A5&isCleanCache=false')
        
        maDataText = json.loads(bcmethod.htmlgetter().geturl(url))['returnValues']['value']
        data = maDataText.split('=')
        
        i = Days.index(days) + 3
        maData = data[i].split(';')
        MaData = maData[0].split(',')
        MaData = MaData[::-1]
        
        for j in range(len(MaData)):
            if MaData[j] == dateTS:
                return float(MaData[j-1][0:-2])
                break