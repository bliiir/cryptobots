import json
import pprint
import time
from datetime import datetime

symbols = ['ETHUSDT', 'BTCUSDT', 'NEOUSDT', 'LTCUSDT']

###
### Classes
###

# Create a new renko block
class renko_block:
    def __init__(self, pair, block_count, time_open, time_close, price_open, price_close, signal):
        self.pair = pair
        self.block_count = block_count
        self.time_open = time_open
        self.time_close = time_close
        self.price_open = price_open
        self.price_close = price_close
        self.signal = signal

        '''WRITE THE BLOCK TO THE DB'''

    return vars(self)

# Create a new renko block manager
class renko_block_manager(object):
    def __init__(self):
        self.pair = 'GET PAIR FROM BOT OBJECT'
        self.chain = []
        self.block_count = 0

    def add_new_block(self, pair, time_open, time_close, price_open, price_close, signal):
        self.block_count += 1
        block = renko_block(self.block_count, time_open, time_close, price_open, price_close, signal)
        self.chain.append(block)
        '''WRITE A BLOCK TO THE DB'''

        return vars(block)

    def get_previous_block(self):
        '''READ LAST BLOCK FROM THE DB'''
        return vars(self.chain[-1])

    # def pretty_print(self, width):
        #pp = pprint.PrettyPrinter(indent=4, width=width, depth=None, stream=None)
        #pp.pprint(self)

# Create a currency pair object and the methods used to update and query it
# NEEDS DB AND PRICE LOOPER
class pair:
    def __init__(self, symbol):
        self.symbol = symbol
        self.price_current = None
        self.timestamp_current = None
        self.price_prev = None
        self.timestamp_prev = None
        self.timestamp_created = int(time.time())
        return vars(self)

    def update(self):
        self.price = 'READ THE LATEST PRICE FROM THE DB THE PRICE LOOPER WRITES'
        self.timestamp = 'READ THE LATEST TIME FROM THE DB THE PRICE LOOPER WRITES'
        return vars(self)

    def prev(self):
        print('')
        self.price_previous =  'READ THE PREVIOUS PRICE FROM THE DB'
        self.timestamp_previous = 'READ THE PREVIOUS TIMETAMP FROM THE DB'
        return (self.symbol, self.price_previous, timestamp_previous)

    def get(self): return vars(self)

# Create an asset object and the methods used to update and query it
class asset:
    def __init__(self, ticker):
        self.ticker = ticker
        self.balance_local = None
        self.balance_global = None

    def update(self, time, asset_delta):
        self.balance_local += delta
        self.balance_global = # UPDATE ALL BALANCES FROM EXCHANGE IN THE DB AND THEN READ THE SPECIFIC ASSET BALANCE FROM DB
        return self.balance_local

    def get(self): return vars(self)




###
### Functions
###



###
###
###



# Create pair objects
pair[] =
for symbol in symbols:
    pair[symbol] = pair(symbol)
    #create traders for all the pairs you want to trade
'''


class renko_trader:

    def __init__(self, manager):
        self.manager = manager

    def get_signal(self):
        i = len(self.manager.chain) - 1
        if i <= 0: return "Hold"

        if self.manager.chain[i].signal is 1:
            # Execute buy order method
            return "BUY"

        elif self.manager.chain[i].signal is 0:
            # Execute sell order method
            return "SELL"

        else: raise Exception('Renko chain is corrupted')

'''


''' PARKED BELOW '''

'''

If current price is 5% higher than the closing price of the previous block then create new block with a "Buy" signal and execute a buy market order
If current price is 5% lower than the closing price of the previous block then create new block with a "sell" signal and execute a buy market order



my_manager = renko_block_manager()
my_manager.add_new_block(1,2,3,4,5)

my_trader = renko_trader(my_manager)


class order:
    def __init__(self, asset, peg, quantity):
        self.order_id = str(uuid.uuid4())
        self.symbol = str(asset+peg)
        self.quantity = str(quantity)
        self.status = 'NEW'

    def market_buy():
        self.type = 'MARKET'
        self.side = 'BUY'

        try: order = client.order_market_buy(symbol = self.symbol, quantity = sel.quantity)
        except Exception as e: print(e)

        while True:
            self.status = self.order_status(self.order_id)
            if self.status is not "NEW":
                return vars(self)
                break

        #Get New asset balances and return those as well?

        asset_delta = None
        peg_delta = None
        return vars(self)

    def market_sell():
        self.type = 'MARKET'
        self.side = 'SELL'

    def limit_buy(price):
        self.price = price
        self.type = 'MARKET'
        self.side = 'SELL'
        print('')

    def limit_sell():
        self.price = price
        print('')

    def test_buy():
        print('')

    def test_sell():
        print('')

    def order_status(order_id):
        print('')

    def balance(symbol):
        print('')


class account:
    def __init__():
        print('')

    def update_asset_balance_local():
        print('')

    def update_peg_balance_local():
        print('')

    def get_asset_balance_local():
        print('')

    def get_peg_balance_local():
        print('')






manager1 = renko_block_manager()

my_blocks = []

for i in range(1,10):
    block = manager1.add_new_block(i,i,i,i,1)
    my_blocks.append(block)
    #print(manager1.block_count, block)
#print(json.dumps(my_blocks, indent=1))
renko_block_manager.pretty_print(my_blocks, 180)

#trader = renko_trader(manager1)
#print(trader.update())









manager1 = Renko_block_manager() # Create a new renko manager
manager1.add_new_block(1) # Create a new block with the manager

manager2 = Renko_block_manager()
manager2.add_new_block(1)


renko1 = renko_trader(manager1) # Create a new renko trader with a new manager
renko2 = renko_trader(manager2)

bots = [renko1, renko2]

for bot in bots:
    print("Bot:" + str(bot.update()))

manager1.update(-1)
manager2.update(1)


for bot in bots:
    print("Bot:" + str(bot.update()))
'''
