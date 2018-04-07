import sys
from binance.client import Client
import credentials
import time

import datetime
import uuid
import logging


'''
Test: python3 renko_006.py ETH 0.002 0.02 11009.9900 USDT 2 20.0 1.0005 1.0
Real: python3 renko_006.py BTC 0.001 0.01 11009.9900 USDT 10 100.0 1.05 1.0

'''

asset_base          = str(sys.argv[1])
asset_base_min      = round(float(sys.argv[2]), 4)
asset_base_bal_loc  = round(float(sys.argv[3]), 4)
price_begin         = round(float(sys.argv[4]), 4) # comment out if you want to set the beginning price automatically and then remove # from the price_begin initialisation further down

asset_quota         = str(sys.argv[5])
asset_quota_min     = round(float(sys.argv[6]), 4)
asset_quota_bal_loc = round(float(sys.argv[7]), 4)

trigger             = round(float(sys.argv[8]), 4)
trade_size          = round(float(sys.argv[9]), 4)

pair = asset_base + asset_quota


client = Client(credentials.key_api_trade_binance, credentials.secret_api_trade_binance) # Connect with Binance.client account API

# Setup log
now = datetime.datetime.now()
log_file = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S") + ' %s' % pair + '.log'
logging.basicConfig(filename=log_file ,level=logging.INFO)

# Create the block
class block():
    def __init__(self, pair, price_begin):
        self.pair               = pair
        self.side               = None
        self.price_open         = float(price_begin)
        self.price_close        = float(price_begin)
        self.target_buy         = float(self.price_close * trigger)
        self.target_sell        = float(self.price_close * 1/trigger)
        self.block_count        = 0

        log_str = 'Block: %i' % self.block_count + ' po: %.2f ' % self.price_open + ' pc: %.2f' % self.price_close + ' tb: %.2f' % self.target_buy + ' ts: %.2f' % self.target_sell + ' %s ' % self.side
        logging.info(log_str)

    def write(self, side):

        if self.side is None :
            if side is 'BUY':
                price_open      = float(self.price_close)
                price_close     = float(price_open * trigger)
                target_buy      = float(price_close * trigger)
                target_sell     = float(price_open * 1/trigger)
            elif side is 'SELL':
                price_open      = float(self.price_close)
                price_close     = float(price_open * 1/trigger)
                target_buy      = float(price_open * trigger)
                target_sell     = float(price_close * 1/trigger)

        if self.side is 'BUY' :
            if side is 'BUY':
                price_open      = float(self.price_close)
                price_close     = float(price_open * trigger)
                target_buy      = float(price_close * trigger)
                target_sell     = float(price_open * 1/trigger)
            elif side is 'SELL':
                price_open      = float(self.price_open)
                price_close     = float(price_open * 1/trigger)
                target_buy      = float(price_open * trigger)
                target_sell     = float(price_close * 1/trigger)

        if self.side is 'SELL':
            if side is 'BUY':
                price_open      = float(self.price_open)
                price_close     = float(price_open * trigger)
                target_buy      = float(price_close * trigger)
                target_sell     = float(price_close * 1/trigger)
            if side is 'SELL':
                price_open      = float(self.price_close)
                price_close     = float(price_open * 1/trigger)
                target_buy      = float(price_open * trigger)
                target_sell     = float(price_close * 1/trigger)

        self.side               = side
        self.price_open         = price_open
        self.price_close        = price_close
        self.target_buy         = target_buy
        self.target_sell        = target_sell

        self.block_count        += 1

        log_str = 'Block: %i' % self.block_count + ' po: %.2f ' % self.price_open + ' pc: %.2f' % self.price_close + ' tb: %.2f' % self.target_buy + ' ts: %.2f' % self.target_sell + ' %s ' % self.side
        logging.info(log_str)

        return vars(self)

    def read(self):
        return vars(self)


class balances():
    def __init__(self, asset_base, asset_quota):
        self.asset_base             = asset_base
        self.asset_quota            = asset_quota
        self.asset_base_bal_loc     = float(asset_base_bal_loc)
        self.asset_quota_bal_loc    = float(asset_quota_bal_loc)

    def write(self, asset_base_delta, asset_quota_delta):

        self.asset_base_bal_loc     += float(asset_base_delta)
        self.asset_quota_bal_loc    += float(asset_quota_delta)

    def read(self):

        while True:
            try:
                self.asset_base_bal_glo     = float(client.get_asset_balance(asset=asset_base)['free'])
                self.asset_quota_bal_glo    = float(client.get_asset_balance(asset=asset_quota)['free'])
                break
            except Exception as e:
                print('connection error while trying to update get global balances', e)
                continue

        # Check if local balances are higher than global and set them equal to global if they are.
        if self.asset_base_bal_glo <= self.asset_base_bal_loc:
            self.asset_base_bal_loc = float(self.asset_base_bal_glo)

        if self.asset_quota_bal_glo <= self.asset_quota_bal_loc:
            self.asset_quota_bal_loc = float(self.asset_quota_bal_glo)

        return vars(self)

def get_pairs(): # Get the prices from Binance
    pairs = [] # reset pairs list
    try:
        binance_snapshot = client.get_all_tickers()
        for each in binance_snapshot: # Store them in a list
            pairs.append(each)
    except Exception as e:
        print('connection error while trying to get price list from Binance', e)
    return pairs


def get_price(pair, pairs): # Get the price for the pair in question
    for item in pairs:
        if str.upper(item['symbol']) == str.upper(pair):
            price = float(item['price'])
    return price


def market_order(pair, quantity, side):

    asset_base_delta = 0
    asset_quota_delta = 0

    if side is 'SELL': sign = -1
    elif side is 'BUY': sign = 1

    while True:
        try:
            order = client.create_order(symbol = pair, side = side, quantity = round(quantity, 4), type = 'MARKET', newOrderRespType = 'FULL')

            for each in order['fills']:
                asset_base_delta    +=  sign * float(each['qty'])
                asset_quota_delta   += -sign * float(each['qty']) * float(each['price']) - float(each['commission'])

            my_balance.write(asset_base_delta, asset_quota_delta)

            break

        except Exception as e:
            log_str = 'Error while trying to execute market order: ' + str(e)
            logging.warning(log_str)
            order = None
            break

    log_str = 'asset_base_delta: %.4f ' % asset_base_delta + ' asset_quota_delta: %.4f ' % asset_quota_delta
    logging.info(log_str)

    return {'asset_base_delta': asset_base_delta,'asset_quota_delta': asset_quota_delta}


# Initialize
i = 0
order = None
my_balance = balances(asset_base, asset_quota)
pairs = get_pairs()
#price_begin = get_price(pair, pairs) # Remove the # if you want the opening price to be set to current price
this_block = block(pair, price_begin)


while True:
    i += 1

    price = get_price(pair, get_pairs())

    side = this_block.read()['side']
    price_open = this_block.read()['price_open']
    price_close = this_block.read()['price_close']
    target_buy = this_block.read()['target_buy']
    target_sell = this_block.read()['target_sell']
    price_target_buy = this_block.read()['target_buy']
    price_target_sell = this_block.read()['target_sell']

    asset_base_bal_loc = my_balance.read()['asset_base_bal_loc']
    asset_quota_bal_loc = my_balance.read()['asset_quota_bal_loc']
    asset_base_bal_glo = my_balance.read()['asset_base_bal_glo']
    asset_quota_bal_glo = my_balance.read()['asset_quota_bal_glo']
    order_size_buy = my_balance.read()['asset_quota_bal_loc'] / price * trade_size
    order_size_sell  = my_balance.read()['asset_base_bal_loc'] * trade_size

    time_cur = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")

    # Log iteration - PUT IN TIMESTAMP!!!
    log_str = format(i, '06d') + ' %s' % time_cur + ' P: %.4f' % price + ' PO: %.4f' % price_open + ' PC: %.4f' % price_close + ' TB: %.4f' % target_buy + ' TS: %.4f' % target_sell + ' BL: %.4f' % asset_base_bal_loc + ' QL: %.4f' % asset_quota_bal_loc + ' BG: %.4f' % asset_base_bal_glo + ' QG: %.4f' % asset_quota_bal_glo + ' SIDE: %s' % side
    logging.info(log_str)


    if price >= price_target_buy:
        side = 'BUY'
        this_block.write(side)

        if asset_quota_bal_loc < asset_quota_min: # Check if we have enough quota to execute the buy
            logging.warning('Not enough %s ' % asset_quota)
            continue
        else:
            order = market_order(pair, order_size_buy, side)
            logging.info('New ' + side + ' order for %.4f' % order_size_buy + ' ' + asset_base)

    if price <= price_target_sell:
        side = 'SELL'
        this_block.write(side)

        if asset_base_bal_loc < asset_base_min: # Check if we have enough asset to execute the sale
            logging.warning('Not enough %s ' % asset_base)
            continue
        else:
            order = market_order(pair, order_size_sell, side)
            logging.info('New ' + side + ' order for %.4f' % order_size_sell + ' ' + asset_base)

    time.sleep(5)
