#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Screen Stocks
Type: Tool
Auther: Arda
"""
# Public modules
from bs4 import BeautifulSoup
import datetime
import time

# My modules
import basiccarwlmethod as bcmethod
import permit2trade as p2t
import techanalysis as ta


# Return stocks whose amplitude is above 5% 
# and match the Price & Volume conditions.
def amplitudefilter(rowData):
    soup = BeautifulSoup(rowData, 'html.parser')
    
    # Check date of data. (WebDate == Today)
    # Web update date.
    timeelement = soup.find_all('time', {'class':'update'})
    date = timeelement[0].text.split(' ')
    # Today
    today = str(datetime.datetime.now().date())
    today = today[0:4] + '/' + today[5:7] + '/' + today[8:10]

    if not (date[0] == today):
        print('Warning!!\nLast time the web data update is ' + date[0] + ', not today.')
    else:
        print('Last time the web data update is today: ' + date[0])
        
    AmpFilterResult = []
    
    Data1 = soup.find_all('div', {'class':'mainCont'})
    Data2 = Data1[0].find_all('tbody')
    Stocks = Data2[0].find_all('tr')
    
    for stock in Stocks:
        Info = stock.find_all('td')
        
        stockNum = Info[0].a.text
        stockName = Info[1].a.text
        stockPrice = float(Info[2].text)
        stockAmp = float(Info[6].text)
        stockVol = int(Info[9].text)
        
        if len(stockNum) == 4 and stockAmp >= 5.0:
            if stockPrice >= 10.0 and stockPrice <= 25.0 and stockVol >= 10000:
                AmpFilterResult.append([stockNum, stockName, stockPrice,
                                        str(stockAmp) + '%', stockVol])
            elif stockPrice >= 50.0 and stockPrice <= 68.0 and stockVol >= 8000:
                AmpFilterResult.append([stockNum, stockName, stockPrice,
                                        str(stockAmp) + '%', stockVol])
            elif stockPrice >= 100.0 and stockPrice <= 408.0 and stockVol >= 6000:
                AmpFilterResult.append([stockNum, stockName, stockPrice,
                                        str(stockAmp) + '%', stockVol])
            elif stockPrice >= 500.0 and stockVol >= 4000:
                AmpFilterResult.append([stockNum, stockName, stockPrice,
                                        str(stockAmp) + '%', stockVol])
    
    return AmpFilterResult   
   
    
def main():  
    date = '20180831'
    urlAmp = 'https://www.wantgoo.com/stock/twstock/stat?type=amplitude'
    StockCandidate = amplitudefilter(bcmethod.htmlgetter().geturl(urlAmp))
    
    #StockCandidate = p2t.permission().sbmsbellowpar(StockCandidate, date)
    StockCandidate = p2t.permission().daytradeable(StockCandidate, date)
    StockCandidate = p2t.permission().cansellb4buy(StockCandidate, '20180903')
  
    DayTradeCandidate = []
    for stock in StockCandidate:
        time.sleep(4)
        rsi = ta.techmethod().rsi(stock[0], date, 5)
        if rsi < 85.0 and rsi > 15.0:
            stock.append(rsi+'%')
            DayTradeCandidate.append(stock)
        time.sleep(3)
    
    for stock in DayTradeCandidate:
        print(stock)
          
    
if __name__ == '__main__':
    main()