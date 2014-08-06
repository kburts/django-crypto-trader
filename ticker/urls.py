from django.conf.urls import patterns, url

from .views import IndexView, ChartView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view()),
    url(r'^chart/$', ChartView.as_view())
)