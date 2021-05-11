from django.db import models
from rest_framework import filters as filter_backends, viewsets
from django_filters import rest_framework as filters


class StockPortfolio(models.Model):
    name = models.CharField(max_length=255, null=True)
    sector = models.CharField(max_length=255, null=True)

class Stock(models.Model):
    ticker = models.CharField(max_length=255)
    current_price = models.DecimalField(decimal_places=1, max_digits=16)
    portfolio = models.ManyToManyField(to=StockPortfolio, on_delete=models.deletion.CASCADE, related_name='stocks')


class PortfolioLookupFilterBackend(filter_backends.BaseFilterBackend):
    additional_fields = ['stocks_and', 'stocks_or', 'stocks_exclude']

    def filter_queryset(self, request, queryset, view):
        # solution goes here
        query_params = request.query_params  # a dict of  {'url_param_1': url_value_1, ...}
        return queryset

class PortfolioViewset(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, PortfolioLookupFilterBackend)
    queryset = StockPortfolio.objects.all()


# todo Q1:
# Right now, this basic DRF viewset would allow for querying for Portfolios and filtering using the DjangoFilterBackend.
# So, we'd be able to use URLs like http://127.0.0.1:8000/portfolio/?name=top_stock_picks
#
# We want to extend this filtering to be able to filter based on Stock Ids.
# So, we create a custom FilterBackend that extends the BaseFilterBackend and overrides the filter_queryset method.
# The goal is to have our URL accept the following arguments: 'stocks_and', 'stocks_or', 'stocks_exclude'
# These arguments will take a CSV list of Stock Ids in the URL.
#
# examples:
# Consider Portfolio 1 has stocks with ids [123, 456, 789]. Portfolio 2 has stocks with ids [123, 300, 789].
# So, input URL -> queryset output
# http://127.0.0.1:8000/portfolio/?stocks_and=123 -> Portfolios [1,2]
# http://127.0.0.1:8000/portfolio/?stocks_and=123,789 -> Portfolios [1,2]
# http://127.0.0.1:8000/portfolio/?stocks_and=123,300 -> Portfolios [2]
# http://127.0.0.1:8000/portfolio/?stocks_and=123,900 -> Portfolios []

# http://127.0.0.1:8000/portfolio/?stocks_or=456,300 -> Portfolios [1,2]
# http://127.0.0.1:8000/portfolio/?stocks_or=456,900 -> Portfolios [1]

# http://127.0.0.1:8000/portfolio/?stocks_exclude=456,900 -> Portfolios [2]
# http://127.0.0.1:8000/portfolio/?stocks_exclude=123 -> Portfolios []

# http://127.0.0.1:8000/portfolio/?stocks_and=123,789&stocks_exclude=456 -> Portfolios [2]