#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Trading
Type: Tool
Auther: Arda
"""

class estimatetool:
    # Target price estimating (tgt est)
    # Call tgtest as tgtest(manageTrend, inPrice) => tgtest(str, float)
    # for example tgtest('bull', 25.5)
    # Return a float, for example, 25.75 means target price = 25.75 .
    def tgtest(self, manageTrend, inPrice):
        tickGap = [0.05, 0.1, 0.5]
        
        if manageTrend == 'bull':
            buyPrice = inPrice
            estPrice = 1.011*buyPrice
        
            if estPrice < 50:
                tick = 5 if int(0.011*buyPrice/tickGap[0]) > 5 else int(0.011*buyPrice/tickGap[0])
                sellPrice = buyPrice + float(tick) * tickGap
                outPrice = sellPrice if sellPrice > 1.0058761*buyPrice else 0
            elif estPrice < 100 and estPrice >= 50:
                tick = 5 if int(0.011*buyPrice/tickGap[1]) > 5 else int(0.011*buyPrice/tickGap[1])
                sellPrice = buyPrice + float(tick) * tickGap
                outPrice = sellPrice if sellPrice > 1.0058761*buyPrice else 0
            elif estPrice < 500 and estPrice >= 100:
                tick = 5 if int(0.011*buyPrice/tickGap[2]) > 5 else int(0.011*buyPrice/tickGap[2])
                sellPrice = buyPrice + float(tick) * tickGap
                outPrice = sellPrice if sellPrice > 1.0058761*buyPrice else 0
        
        elif manageTrend == 'bear':
            sellPrice = inPrice
            estPrice = 0.989*sellPrice
            
            if estPrice < 50:
                tick = 5 if int(0.011*sellPrice/tickGap[0]) > 5 else int(0.011*sellPrice/tickGap[0])
                buyPrice = sellPrice - float(tick) * tickGap
                outPrice = buyPrice if sellPrice > 1.0058761*buyPrice else 0
            elif estPrice < 100 and estPrice >= 50:
                tick = 5 if int(0.011*sellPrice/tickGap[1]) > 5 else int(0.011*sellPrice/tickGap[1])
                buyPrice = sellPrice - float(tick) * tickGap
                outPrice = buyPrice if sellPrice > 1.0058761*buyPrice else 0
            elif estPrice < 500 and estPrice >= 100:
                tick = 5 if int(0.011*sellPrice/tickGap[2]) > 5 else int(0.011*sellPrice/tickGap[2])
                buyPrice = sellPrice - float(tick) * tickGap
                outPrice = buyPrice if sellPrice > 1.0058761*buyPrice else 0
     
        return outPrice
    
    
    # Volume estimating (vol est)
    # Call volest as volest(closePrice, targetPrice, closeVol) => volest(float, float, int)
    # for example volest(24.0, 25.5, 1000)
    # Return (int, int), for example, .
    def volest(self, closePrice, targetPrice, closeVol):
        profitVal = 0.995575*targetPrice - 1.001425*closePrice
       
        if closePrice < 50:
            coeff = 3.0 if (float(closeVol)/10000.0) > 3.0 else (float(closeVol)/10000.0) 
            tradeVol = (1000.0 - profitVal) * coeff
        elif closePrice >= 50 and closePrice < 100:
            coeff = 3.0 if (float(closeVol)/8000.0) > 3.0 else (float(closeVol)/8000.0) 
            tradeVol = (2000.0 - profitVal) * coeff
        elif closePrice >= 100 and closePrice < 500:
            coeff = 3.0 if (float(closeVol)/6000.0) > 3.0 else (float(closeVol)/6000.0) 
            tradeVol = (4000.0 - profitVal) * coeff
        
        return int(tradeVol), int(float(closeVol)*5.0/13.0)

  
    # RSI safe range estimating (safe rsi est)
    # Call safersiest as safersiest(rsiHigh, rsiLow) => safersiest(float, float)
    # for example safersiest(10.5, 87.5)
    # Return (float, float, float, float), for example, .
    def safersiest(self, rsiHigh, rsiLow):
        highRigRSI = 100.0 - 2.0*(100.0-rsiHigh)
        lowRigRSI = 2.0*rsiLow
        highLosRSI = 100.0 - 1.5*(100.0-rsiHigh)
        lowLosRSI = 1.5*rsiLow
        
        return highRigRSI, lowRigRSI, highLosRSI, lowLosRSI
        