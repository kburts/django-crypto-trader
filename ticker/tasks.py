import time
import requests

from django_cryptos.celery import app
from .models import Exchange, Pair, Ticker


@app.task
def hello_world():
    print('Hello world')

@app.task
def pollAPI(pair):
    """
    exchange: exchange name
    @param: pair Pair object
    """
    url = pair.get_api_endpoint_url()
    request = requests.get(url).json()

    for item in pair.get_price_json_location():
        request = request.get(item)

    Ticker.objects.create(pair=pair, timestamp=time.time(), price=request)

@app.task
def pollAllAPI():
    """
    Polls all external API's in a list
    """
    pairs = Pair.objects.all()
    for pair in pairs:
        pollAPI.delay(pair)


@app.task
def createCSV(pairpk):
    """
    Create .csv file for a pair.
    """
    data = Ticker.objects.filter(pair=pairpk)
    out = []
    outfile = "ticker/static/ticker/csv.csv"
    for item in reversed(data):
        out.append('%s,%s\n' %(item.timestamp, item.price))
    with open(outfile, 'w') as f:
        f.write("time,price\n")
        for item in out:
            f.write(item)


@app.task
def fillDataHoles():
    """
    Attempts to fill holes in data caused by server shutdown,
        or unavailability to connect to the external API
    Might take a long time!
    """
    pass