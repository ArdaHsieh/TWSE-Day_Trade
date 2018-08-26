#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Screen Stocks
Type: Tool
Auther: Arda
"""

import requests
import json
from bs4 import BeautifulSoup


def geturl():
    url = 'https://www.wantgoo.com/stock/twstock/stat?type=amplitude'
    return requests.get(url).text.encode('utf-8-sig')


def amplitudefilter(StockCandidate):
    soup = BeautifulSoup(StockCandidate, 'html.parser')
    data1 = soup.find_all('div', {'class':'mainCont'})
    