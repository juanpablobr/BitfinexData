
from Controllers.BfxDataLoader import BfxDataLoader
from Api.BfxApiModel           import *
from Database.DatabaseModel    import DatabaseModel

import pandas as pd
from ta import *

data = BfxDataLoader(debug=True)

data.load(Symbols.BTC_USD, TimeFrames.D1)
data.load(Symbols.BTC_USD, TimeFrames.h1)
data.load(Symbols.BTC_USD, TimeFrames.m15)

db = DatabaseModel()
df = db.df("Bfx_tBTCUSD_15m")

df['Stochastic'] = stoch_signal(df['high'], df['low'], df['close'])

print(df)
