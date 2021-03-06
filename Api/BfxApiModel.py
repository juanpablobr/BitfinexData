
from enum import Enum
import requests

class Symbols(Enum):
    BTC_USD = "tBTCUSD"
    LTC_BTC = "tLTCBTC"

class TimeFrames(Enum):
    m1  = "1m"
    m15 = "15m"
    h1  = "1h"
    D1  = "1D"
    M1  = "1M"

class Sections(Enum):
    last = "last"
    hist = "hist"

class Sort(Enum):
    newFirst = 0
    oldFirst = 1

class BfxApiModel:
    baseUrl    = "https://api.bitfinex.com/"
    apiVersion = "v2/" 
    def __init__(self, debug=False):
        self.apiUrl = self.baseUrl + self.apiVersion
        self.debug  = debug

    # Public Endpoints
    # 1=operative, 0=maintenance
    def platformStatus(self):
        resourse = "platform/status"
        url      = self.apiUrl + resourse
        response = self.__sendGetRequest(url)
        return response

    def symbols(self):
        raise NotImplementedError

    def tickers(self):
        raise NotImplementedError

    def ticker(self, symbol: Symbols):
        resourse = "ticker/" + symbol.value
        url      = self.apiUrl + resourse
        response = self.__sendGetRequest(url)
        return response

    def trades(self):
        raise NotImplementedError
    
    def books(self):
        raise NotImplementedError
    
    def stats(self):
        raise NotImplementedError

    def candles(self, timeframe: TimeFrames, symbol: Symbols, start: int, end: int, section=Sections.hist,nOfCadles=100,sort=Sort.newFirst):
        resourse = "candles/trade:" + timeframe.value + ":" + symbol.value + "/" + section.value 
        url      = self.apiUrl + resourse
        params   = {
            'limit': nOfCadles,
            'start': start,
            'end'  : end,
            'sort' : sort.value  
        }
        response = self.__sendGetRequest(url, params=params)
        return response

    # Private functions
    def __sendGetRequest(self, url: str, params=None):
        r = requests.get(url, params=params)
        if self.debug:
            print(r.url)
        return r.json()
