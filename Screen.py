#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Screen Stocks
Type: Tool
Auther: Arda
"""
# Public package
import requests
from bs4 import BeautifulSoup
import datetime

# My package
import permit2trade as p2t
#import techanalysis as tanal


# Request web page with url and method get.
def geturl(url):
    headers = {
               'user-agent': 'Mozilla/5.0 (Windows NT 6.1)'
                           + 'AppleWebKit/537.36 (KHTML, like Gecko)'
                           + 'Chrome/52.0.2743.116 Safari/537.36'
              }
    
    return requests.get(url, headers = headers).text.encode('utf-8-sig')


# Return stocks whose amplitude is above 5% 
# and match the Price & Volume conditions.
def amplitudefilter(rowData):
    soup = BeautifulSoup(rowData, 'html.parser')
    
    # Check date of data. (WebDate == Today)
    # Web update date.
    time = soup.find_all('time', {'class':'update'})
    date = time[0].text.split(' ')
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
    
    return AmpFilterResult, date[0]  
   
    
def main():    
    urlAmp = 'https://www.wantgoo.com/stock/twstock/stat?type=amplitude'
    StockCandidate, date = amplitudefilter(geturl(urlAmp))
    StockCandidate = p2t.permission().sbmsbellowpar(StockCandidate, '20180830')
    StockCandidate = p2t.permission().daytradeable(StockCandidate, '20180830')
    StockCandidate = p2t.permission().cansellb4buy(StockCandidate, '20180830')
    
    print(StockCandidate)
    
    
    
if __name__ == '__main__':
    main()