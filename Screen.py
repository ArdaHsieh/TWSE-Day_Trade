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
import pandas as pd

# My modules
import basiccrawlmethod as bcmethod
import permit2trade as p2t
import techanalysis as ta
import parmsetting as parm


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
    closeDay = input("Stock close day(yyyymmdd): ")
    tradeDay = input("Trade day(yyyymmdd): ")
    urlAmp = 'https://www.wantgoo.com/stock/twstock/stat?type=amplitude'
    StockCandidate = amplitudefilter(bcmethod.htmlgetter().geturl(urlAmp))
    
    #StockCandidate = p2t.permission().sbmsbellowpar(StockCandidate, date)
    StockCandidate = p2t.permission().daytradeable(StockCandidate, tradeDay)
    #StockCandidate = p2t.permission().cansellb4buy(StockCandidate, '20180903')
  
    AfterRSICandidate = []
    for stock in StockCandidate:
        rsi = ta.techmethod().rsi(stock[0], closeDay, 5)
        if rsi < 85.0 and rsi > 15.0:
            stock.append(str(rsi)+'%')
            AfterRSICandidate.append(stock)
                   
    for stock in AfterRSICandidate:
        maParm = parm.getparm().maparm(stock[0], closeDay)
        stock.append(maParm)
        if maParm[0] < 1.10:
            stock[-1].append('Bear Only')
        elif maParm[1] < 1.10:
            stock[-1].append('Bull Only')
        else:
            stock[-1].append('Bull&Bear')
        
        stock.append(parm.getparm().bbandsparm(stock[0], float(stock[3][0:-1]), closeDay))
    
    BearCandidate = [] 
    for stock in AfterRSICandidate:
        if stock[6][2] == 'Bear Only':
            BearCandidate.append(stock)
    
    BearCandidate = p2t.permission().cansellb4buy(BearCandidate, tradeDay)
        
    DayTradeCandidate = []
    for stock in AfterRSICandidate:
        if stock[6][2] != 'Bear Only' or stock in BearCandidate:
            DayTradeCandidate.append(stock)
    
    (Number, Name, Price, Amplitude, Volume, RSI, MA_top_parm, MA_buttom_parm,
    Trend, BBand_parm, BBand_wide) = ([], [], [], [], [], [], [], [], [], [], [])
    for stock in DayTradeCandidate:
        Number.append(stock[0])
        Name.append(stock[1])
        Price.append(stock[2])
        Amplitude.append(stock[3])
        Volume.append(stock[4])
        RSI.append(stock[5])
        MA_top_parm.append(stock[6][0])
        MA_buttom_parm.append(stock[6][1])
        Trend.append(stock[6][2])
        BBand_parm.append(stock[7][0])
        BBand_wide.append(stock[7][1])
    
    CanDataFrame = {
                    'Number' : Number,
                    'Name' : Name,
                    'Price' : Price,
                    'Amplitude' : Amplitude,
                    'Volume' : Volume,
                    'RSI' : RSI,
                    'MA_top_parm' : MA_top_parm,
                    'MA_buttom_parm' : MA_buttom_parm,
                    'Trend' : Trend,
                    'BBand_parm' : BBand_parm,
                    'BBand_wide' : BBand_wide
                   } 
    CanColumns = ['Number', 'Name', 'Price', 'Amplitude', 'Volume', 'RSI',
                  'MA_top_parm', 'MA_buttom_parm', 'Trend', 'BBand_parm', 'BBand_wide']
    
    Candidate = pd.DataFrame(CanDataFrame, columns = CanColumns)
    Candidate.to_csv('Candidate' + tradeDay + '.csv', encoding='big5')
          
    
if __name__ == '__main__':
    main()