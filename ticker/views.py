from django.shortcuts import render
from django.views.generic import TemplateView

from .tasks import hello_world

# Create your views here.

class IndexView(TemplateView):
    template_name = 'ticker/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        hello_world.delay()
        return context

class ChartView(TemplateView):
    template_name = 'ticker/chart.html'