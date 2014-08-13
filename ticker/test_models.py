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

    def test_exchange_unicode(self):
        ex1 = Exchange.objects.get(name="exchange1")
        self.assertEqual(ex1.name, str(ex1))

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
        exchange = Exchange.objects.create(
            name="exchange1",
            url="http://url.com/*_*",
            priceJsonLoc="last"
        )
        currency1 = Currency.objects.create(
            name="bitcoins",
            symbol="btc"
        )
        currency2 = Currency.objects.create(
            name="dollars",
            symbol="usd"
        )
        Pair.objects.get_or_create(
            exchange = exchange,
            currency1 = currency1,
            currency2 = currency2
        )
        ex = Exchange.objects.get(name="exchange1")
        self.pair = Pair.objects.get(exchange=ex)

    def test_pair_created(self):
        btc_usd = self.pair
        self.assertIsInstance(btc_usd, Pair)

    def test_get_api_endpoint_url(self):
        btc_usd = self.pair
        self.assertEqual(
            btc_usd.get_api_endpoint_url(),
            "http://url.com/btc_usd"
        )
        btc_usd.exchange.url = "http://www.example.com/"
        self.assertEqual(btc_usd.exchange.url, btc_usd.get_api_endpoint_url())

    def test_get_price_json_location(self):
        btc_usd = self.pair
        self.assertEqual(btc_usd.get_price_json_location(), ["last"])