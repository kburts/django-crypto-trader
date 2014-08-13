import time

import requests

from django_cryptos.celery import app
from .models import Pair, Ticker


@app.task
def hello_world():
    print('Hello world')


@app.task
def pollAPI(pair):
    """
    Get exchange data for a single Pair object.
    @param: Pair object
    """
    url = pair.get_api_endpoint_url()
    request = requests.get(url).json()

    for item in pair.get_price_json_location():
        request = request.get(item)

    Ticker.objects.create(pair=pair, timestamp=time.time(), price=request)


@app.task
def pollAllAPI():
    """
    Polls all external API's (every Pair)
    """
    pairs = Pair.objects.all()
    for pair in pairs:
        pollAPI.delay(pair)


@app.task
def createCSV(pairpk):
    """
    Create .csv file for a pair.
    @param: PK Value from a Pair object. eg.2
    """
    data = Ticker.objects.filter(pair=pairpk)
    out = []
    outfile = "ticker/static/ticker/csv.csv"
    for item in reversed(data):
        out.append('%s,%s\n' % (item.timestamp, item.price))
    with open(outfile, 'w') as f:
        f.write("time,price\n")
        for item in out:
            f.write(item)


@app.task
def calcTickersToAdd(ticker1, ticker2, live=False):
    """
    @param: ticker1: later ticker
    @param: ticker2: earlier ticker
    """
    timediff = float(ticker1.timestamp) - float(ticker2.timestamp)
    numToAdd = int(timediff) / 10
    for x in xrange(1, numToAdd):
        timestamp = float(ticker2.timestamp) + 10 * x,
        priceDiff = float(ticker1.price) - float(ticker2.price)
        price = float(ticker2.price) + (priceDiff / x)
        if live:
            Ticker.objects.create(
                pair=ticker1.pair,
                timestamp=timestamp,
                price=price)
        else:
            print ticker1.pair, timestamp, price, ">", ticker1.price, "<>", ticker2.price, "<"


@app.task
def fillDataHoles(pair):
    """
    Check whether there are any gaps in the data.
    @param: Pair object
    """
    allowedDataGap = 15
    data = Ticker.objects.filter(pair=pair.pk)
    for x in xrange(len(data) - 2):  ##all but the last one.
        t1 = float(data[x].timestamp)
        t2 = float(data[x + 1].timestamp)
        ## Check if later timestamp is greater than sooner one by more than 15 seconds
        if t1 > t2 + allowedDataGap:
            calcTickersToAdd(data[x], data[x + 1])
            #timediff = int((t1 - t2)/10)
            #print timediff


@app.task
def fillAllDataHoles():
    """
    Attempts to fill holes in data caused by server shutdown,
        or unavailability to connect to the external API.
    If distance between data points is > 15 seconds, it adds more in the middle.
    Might take a long time!
    """
    pairs = Pair.objects.all()
    for pair in pairs:
        fillDataHoles.delay(pair)
        #fillDataHoles(pair)