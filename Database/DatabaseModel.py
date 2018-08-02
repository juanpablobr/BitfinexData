
import sqlite3
import pandas as pd

class DatabaseModel:
    def __init__(self, dbUrl="./Database/db.sqlite3"):
        self.conn   = sqlite3.connect(dbUrl)
        self.c      = self.conn.cursor()  

    def createTable(self, tableName: str, tableType='''(timestamp INT, open FLOAT, close FLOAT, 
        high FLOAT, low FLOAT, volume FLOAT)'''):
        tableAttr   = tableName + " " + tableType
        createTable = "CREATE TABLE IF NOT EXISTS "

        query       = createTable + tableAttr
        self.c.execute(query)

    def lastTimestamp(self, tableName: str):
        stamp = self.c.execute('SELECT * FROM '+ tableName +' ORDER BY timestamp DESC LIMIT 1')
        return stamp.fetchone()

    def insertCandle(self, tableName: str, candleData: []):

        endIndex = len(candleData)
        valuesArray = []
        for i in range(0, endIndex):
            item = "'" + str(candleData[i]) + "'"
            valuesArray.append(item)

        values   = "(" + ", ".join(valuesArray) + ")"
        insert = "INSERT INTO " + tableName + " VALUES "

        self.c.execute(insert + values)

    def deleteTopRow(self, tableName: str):
        stamp = self.c.execute('SELECT * FROM '+ tableName +' ORDER BY timestamp DESC LIMIT 1')
        selection = stamp.fetchone()
        timestamp = 0
        if selection != None:
            timestamp = selection[0]
        self.c.execute("DELETE FROM "+ tableName +" WHERE timestamp = " + str(timestamp))
        self.conn.commit() 

    def df(self, tableName: str):
        query = "SELECT * FROM " + tableName
        data  = pd.read_sql(sql=query, con=self.conn)
        return data
