#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Screen Stocks
Type: Tool
Auther: Arda
"""
# Public modules
from bs4 import BeautifulSoup
import pandas as pd

# My modules
import basiccrawlmethod as bcmethod
import permit2trade as p2t
import techanalysis as ta
import parmsetting as parm


# Return stocks whose amplitude is above 5% 
# and match the Price & Volume conditions.
def amplitudefilter():
    AmpFilterResult = []
    for i in range(1, 92):
            urlAmp = 'https://histock.tw/stock/rank.aspx?&m=7&p=' + str(i) + '&d=1'
            soup = BeautifulSoup(bcmethod.htmlgetter().geturl(urlAmp), 'html.parser')
            Data1 = soup.find_all('table', {'class':'gvTB'})
            if len(Data1) > 0:
                Data2 = Data1[0].find_all('tr')
                for j in range(1, len(Data2)):
                    Data3 = Data2[j].find_all('td')
                    stockNum = Data3[0].text
                    stockName = Data3[1].a.text
                    stockPrice = float(Data3[2].text)
                    stockAmp = bcmethod.numtrans().strtonum(Data3[7].text)
                    stockVol = bcmethod.numtrans().strtonum(Data3[11].text)/1000.0
                    stockVal = bcmethod.numtrans().strtonum(Data3[13].text)/1000.0
                    
                    if stockAmp >= 5.0:
                        if len(stockNum) == 4:
                            if stockPrice >= 10.0 and stockPrice <= 25.0 and stockVol >= 10000:
                                AmpFilterResult.append([stockNum, stockName, stockPrice, 
                                                        str(stockAmp) + '%', stockVol, stockVal/stockVol])
                            elif stockPrice >= 50.0 and stockPrice <= 68.0 and stockVol >= 8000:
                                AmpFilterResult.append([stockNum, stockName, stockPrice,
                                                        str(stockAmp) + '%', stockVol, stockVal/stockVol])
                            elif stockPrice >= 100.0 and stockPrice <= 408.0 and stockVol >= 6000:
                                AmpFilterResult.append([stockNum, stockName, stockPrice,
                                                        str(stockAmp) + '%', stockVol, stockVal/stockVol])
                            elif stockPrice >= 500.0 and stockVol >= 4000:
                                AmpFilterResult.append([stockNum, stockName, stockPrice,
                                                        str(stockAmp) + '%', stockVol, stockVal/stockVol])
                    else:
                        return AmpFilterResult
            
            else:
                return AmpFilterResult
                    
      
def main():
    closeDay = input("Stock close day(yyyymmdd): ")
    tradeDay = input("Trade day(yyyymmdd): ")
    
    StockCandidate = amplitudefilter()
    
    #StockCandidate = p2t.permission().sbmsbellowpar(StockCandidate, date)
    StockCandidate = p2t.permission().daytradeable(StockCandidate, tradeDay)
  
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
        
        stock.append(parm.getparm().bbandsparm(float(stock[3][0:-1]), stock[5]))
    
    BearCandidate = [] 
    for stock in AfterRSICandidate:
        if stock[6][2] == 'Bear Only':
            BearCandidate.append(stock)
    
    BearCandidate = p2t.permission().cansellb4buy(BearCandidate, tradeDay)
        
    DayTradeCandidate = []
    for stock in AfterRSICandidate:
        if stock[6][2] != 'Bear Only' or stock in BearCandidate:
            DayTradeCandidate.append(stock)
    
    (Number, Name, Price, Amplitude, Volume, MeanPrice, RSI, MA_top_parm, MA_buttom_parm,
    Trend, BBand_parm, BBand_wide) = ([], [], [], [], [], [], [], [], [], [], [], [])
    for stock in DayTradeCandidate:
        Number.append(stock[0])
        Name.append(stock[1])
        Price.append(stock[2])
        Amplitude.append(stock[3])
        Volume.append(stock[4])
        MeanPrice.append(stock[5])
        RSI.append(stock[6])
        MA_top_parm.append(stock[7][0])
        MA_buttom_parm.append(stock[7][1])
        Trend.append(stock[7][2])
        BBand_parm.append(stock[8][0])
        BBand_wide.append(stock[8][1])
    
    CanDataFrame = {
                    'Number' : Number,
                    'Name' : Name,
                    'Price' : Price,
                    'Amplitude' : Amplitude,
                    'Volume' : Volume,
                    'MeanPrice' : MeanPrice,
                    'RSI' : RSI,
                    'MA_top_parm' : MA_top_parm,
                    'MA_buttom_parm' : MA_buttom_parm,
                    'Trend' : Trend,
                    'BBand_parm' : BBand_parm,
                    'BBand_wide' : BBand_wide
                   } 
    CanColumns = ['Number', 'Name', 'Price', 'Amplitude', 'Volume', 'MeanPrice','RSI',
                  'MA_top_parm', 'MA_buttom_parm', 'Trend', 'BBand_parm', 'BBand_wide']
    
    Candidate = pd.DataFrame(CanDataFrame, columns = CanColumns)
    Candidate.to_csv('Candidate' + tradeDay + '.csv', index=0, encoding='big5')
          
    
if __name__ == '__main__':
    main()