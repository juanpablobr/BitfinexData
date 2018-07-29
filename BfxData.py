
from BfxPublicClient import BfxPublicClient
from BfxPublicClient import Symbols
from BfxPublicClient import TimeFrames
from BfxPublicClient import Sort

from Database        import Database

from time            import time
from time            import sleep

class BfxData:
    def __init__(self, dbUrl="./db.sqlite3", tablePrefix="Bfx", debug=False):
        self.debug  = debug 
        self.client = BfxPublicClient(debug=debug)
        self.dbUrl  = dbUrl
        self.tablePrefix = tablePrefix

    def load(self, symbol: Symbols, timeframe: TimeFrames):
        
        db = Database(self.dbUrl)

        frameStr = ""
        if timeframe == TimeFrames.M1:
            frameStr = "1month"
        else:
            frameStr = timeframe.value
        tableName = "_".join([self.tablePrefix, symbol.value, frameStr])
        db.createTable(tableName)

        db.deleteTopRow(tableName)

        stamp = db.lastTimestamp(tableName)
        startTimeStamp = None
        if stamp == None:
            startTimeStamp = 1364774400000
        else:
            startTimeStamp = stamp[0] + 1

        while True:
            
            candles = self.client.candles(timeframe,symbol,startTimeStamp,None,nOfCadles=1000,sort=Sort.oldFirst)

            if candles == ['error', 11010, 'ratelimit: error']:
                if self.debug == True:
                    print(['error', 11010, 'ratelimit: error'])
                sleep(10)
                continue

            candlesLen = len(candles)
            if candlesLen == 0:
                break

            for candle in candles:
                if self.debug == True:
                    print(candle)
                db.insertCandle(tableName ,candle)
                startTimeStamp = candle[0] + 1

            db.conn.commit()

        db.deleteTopRow(tableName)
        db.conn.close()
