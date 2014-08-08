import time
import requests

from django_cryptos.celery import app
from .models import Exchange, Pair, Ticker


@app.task
def hello_world():
    print('Hello world')

@app.task
def pollAPI(*args):
    """
    exchange: exchange name
    curr1/curr2: currency codes eg. btc
    """
    # pair, timestamp, price
    #url = pair.exchange.url
    pair = Pair.objects.get(exchange=args[0], currency1=args[1], currency2=args[2])
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
    exchanges = Exchange.objects.all()
    for exchange in exchanges:
        pairs = Pair.objects.filter(exchange=exchange.pk)
        for pair in pairs:
            pollAPI.delay(pair.exchange.pk, pair.currency1.pk, pair.currency2.pk)


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