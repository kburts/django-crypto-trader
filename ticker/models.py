import time
from django.db import models

# Create your models here.
class Exchange(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField("URL: API endpoint. Replace currencies with *'s.")
    priceJsonLoc = models.CharField(
        "Comma seperated list of location to price in the response eg. 'ticker, last'",
        max_length=200)

    def __unicode__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField("Symbol: Case sensitive", max_length=4)

    def __unicode__(self):
        return self.symbol

class Pair(models.Model):
    exchange = models.ForeignKey(Exchange, related_name="exchanges")
    currency1 = models.ForeignKey(Currency, related_name="currency1")
    currency2 = models.ForeignKey(Currency, related_name="currency2")

    def __unicode__(self):
        return '%s %s %s' %(self.exchange, self.currency1, self.currency2)

    def get_api_endpoint_url(self):
        if not "*" in self.exchange.url:
            return self.exchange.url
        else:
            url = self.exchange.url.replace('*', str(self.currency1), 1)
            url = url.replace('*', str(self.currency2), 1)
            return url

    def get_price_json_location(self):
        loc = self.exchange.priceJsonLoc
        # If it is a list of one item
        if not "," in loc:
            return [loc,]
        loc = loc.split(",")
        for n in range(len(loc)):
            loc[n] = loc[n].strip()
        return loc


class Ticker(models.Model):
    pair = models.ForeignKey(Pair)
    timestamp = models.CharField(max_length=14) #unix time stamp 3 decimal places
    price = models.CharField(max_length=15)

    def __unicode__(self):
        return '%s %s' %(self.pair, self.timestamp)

    class Meta:
        ordering = ['-timestamp'] # newest first.