import logging
import datetime
import exchange
from fileBasedExchangeClient import FileBasedExchangeClient
from fileBasedExchangeClient import FileBasedExchangeClientPriceType
import renkoBot
import renkoBot_plot

##########################################################
# Test parameters
##########################################################

START_CAPITAL = 1000.0
PERCENTAGE = 0.04
START_TIME = datetime.datetime(2017, 1, 1, 1, 0, 0)
END_TIME = START_TIME + datetime.timedelta(days=30)

##########################################################
##########################################################
##########################################################

client = FileBasedExchangeClient(
    'candles-300.csv', FileBasedExchangeClientPriceType.OPEN_CLOSE,
    exchange.ExchangeAsset.USD, exchange.ExchangeAsset.BTC,
    logging.getLogger(),
    {exchange.ExchangeAsset.USD: START_CAPITAL})


bot = renkoBot.RenkoBot(PERCENTAGE, client, logging.getLogger())

while True:
    client.getPrice(exchange.ExchangeAsset.USD, exchange.ExchangeAsset.BTC)
    timestamp = client.getTime()
    if timestamp > START_TIME:
        break

while True:
    bot.tick()
    timestamp = client.getTime()
    if timestamp > END_TIME:
        break


renkoBot_plot.plot(bot, START_CAPITAL)
