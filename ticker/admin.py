from django.contrib import admin

from .models import Exchange, Pair, Currency, Ticker


# Register your models here.

class TickerAdmin(admin.ModelAdmin):
    list_display = ('pair', 'timestamp', 'price')
    list_filter = ('pair',)


admin.site.register(Exchange)
admin.site.register(Pair)
admin.site.register(Currency)
admin.site.register(Ticker, TickerAdmin)