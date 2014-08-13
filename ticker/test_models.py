from django.test import TestCase

from .models import Exchange, Pair, Currency, Ticker

class ExchangeTestCase(TestCase):
    def setUp(self):
        Exchange.objects.get_or_create(
            name="exchange1",
            url="http://www.myexchange.com/api/v1/*_*/ticker/",
            priceJsonLoc="ticker,last"
        )

    def test_exchange_created(self):
        ex1 = Exchange.objects.get(name="exchange1")
        self.assertIsInstance(ex1, Exchange)

class CurrencyTestCase(TestCase):
    def setUp(self):
        Currency.objects.get_or_create(
            name="bitcoin",
            symbol="btc"
        )
        Currency.objects.get_or_create(
            name="dollars",
            symbol="usd" #Should totally be Canadian dollars..
        )

    def test_currency_created(self):
        btc = Currency.objects.get(name="bitcoin")
        self.assertIsInstance(btc, Currency)

    def test_currency_unicode(self):
        btc = Currency.objects.get(name="bitcoin")
        self.assertEqual(str(btc), "btc")

class PairTestCase(TestCase):
    def setUp(self):
        Pair.objects.get_or_create(
            exchange=Exchange.objects.get(name="exchange1"),
            currency1=Currency.objects.get(symbol="btc"),
            currency2=Currency.objects.get(symbol="usd")
        )

    def test_pair_created(self):
        btc_usd = Pair.objects.get(exchange="exchange1")
        self.assertIsInstance(btc_usd, Pair)