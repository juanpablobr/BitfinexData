
from BfxData         import BfxData
from BfxPublicClient import Symbols
from BfxPublicClient import TimeFrames

data = BfxData(debug=True)
data.load(Symbols.BTCUSD, TimeFrames.h1)
data.load(Symbols.BTCUSD, TimeFrames.M1)
data.load(Symbols.BTCUSD, TimeFrames.D1)
data.load(Symbols.BTCUSD, TimeFrames.m1)
