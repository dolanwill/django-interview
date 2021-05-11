from django.db import models
from django.db.models import Count


class StockPortfolio(models.Model):
    name = models.CharField(max_length=255, null=True)

class Stock(models.Model):
    ticker = models.CharField(max_length=255)
    current_price = models.DecimalField(decimal_places=1, max_digits=16)
    portfolio = models.ForeignKey(to=StockPortfolio, on_delete=models.deletion.DO_NOTHING)


# todo Q1:
# Given a StockPortfolio object sp, how can we see what stocks are in that portfolio?

sp = StockPortfolio.objects.first()
# answer here

# todo Q2:
# Write an expression that returns the queryset of portfolios with more than 10 stocks.
# hint: from django.db.models import Count

# answer here
portfolios = StockPortfolio.objects.all()

# todo Q3:
# What will happen right now, to the Stock objects, if a Portfolio they are associated with is deleted?
# What if we wanted the associated Stocks to also delete?