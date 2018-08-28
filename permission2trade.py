#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TWSE permissions of trade.
Type: class, Tool
Auther: Arda
"""

import requests
import json
from bs4 import BeautifulSoup
import datetime


class permission:
    def __init__(self, date):
        self.date = date
        
        
    # Request web page with url and the method GET.
    # Is an inside class function.
    def geturl(self, url):
        headers = {
                   'user-agent': 'Mozilla/5.0 (Windows NT 6.1)'
                               + 'AppleWebKit/537.36 (KHTML, like Gecko)'
                               + 'Chrome/52.0.2743.116 Safari/537.36'
                  }
    
        return requests.get(url, headers = headers).text.encode('utf-8-sig')
    
    
    # Permission for Security-borrowing & Margin-selling bellow price unchange(par).
    # Call sbmsbellowpar as sbmsbellowpar(StockCandidate)
    # StockCandidate must be a 2-D array and start with [0] stock#, [1]stock name.
    # for example, [[#,name1,...], [#,name2,...], [#,name3,...], ...]
    def sbmsbellowpar(self, StockCandidate):
        urlTWSE = "http://www.twse.com.tw/exchangeReport/TWT92U?response=json&date=" + self.date
        htmlJsonTWSE = self.geturl(urlTWSE)
        SBMSData = json.loads(htmlJsonTWSE)['data']
    
        SBMSResult = []
        
        for Candidate in StockCandidate:
            for Stock in SBMSData:
                if Candidate[0] == Stock[0]:
                    if not (Stock[2] == '*' or Stock[3] == '*' or Stock[4] == '*'):
                        SBMSResult.append(Candidate)
                        pass
        
        return SBMSResult
        
