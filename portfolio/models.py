from django.db import models
from django.conf import settings
import requests


# Create your models here.


class DateTimeModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Crypto(models.Model):
    name = models.CharField(max_length=255)
    rate = models.FloatField(default=0)
    change = models.FloatField(default=0)

    def __str__(self):
        return str(self.name)


class Portfolio(DateTimeModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name = models.CharField(max_length=255,unique=True)
    value = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    # gets and returns the current value of the portfolio
    def get_portfolio_value(self):
        updates = UpdatePortfolio.objects.filter(portfolio=self)
        value = 0
        for item in updates:
            value += item.crypto.rate * item.crypto_quantity

        return round(value,2)

    # deletes the portfolio
    def delete_portfolio(self):
        self.delete()

    # gets and returns the total change of portfolio value in USD
    def get_portfolio_change(self):
        change = 0
        total_start_value = 0
        for position in UpdatePortfolio.objects.filter(portfolio=self):
            change += (float(position.get_value()) - float(position.amount_usd))
            total_start_value += position.amount_usd

        try:
            change_percent = (change / total_start_value) * 100
        except ZeroDivisionError:
            change_percent = 0

        return round(change_percent,2)

    # gets and returns portfolio value change in last 24h period
    def get_portfolio_change_24h(self):
        change = 0
        value = self.get_portfolio_value()
        for position in UpdatePortfolio.objects.filter(portfolio=self):
            change += (position.get_value() * position.crypto.change)

        try:
            change_percent = change / value

        except ZeroDivisionError:
            change_percent = 0

        return round(change_percent,2)

    def __str__(self):
        return str(self.name)


class UpdatePortfolio(DateTimeModel):
    amount_usd = models.FloatField(default=100)
    crypto = models.ForeignKey(Crypto,on_delete=models.CASCADE,null=True)
    crypto_quantity = models.FloatField(default=0)
    portfolio = models.ForeignKey(Portfolio,on_delete=models.CASCADE,null=True)

    # gets and returns the value of UpdatePortfolio object
    def get_value(self):
        res = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price?ids={self.crypto.name}&vs_currencies=usd&include_24hr_change=true")
        rate = res.json()[f"{self.crypto.name}"]["usd"]
        value = round(rate * self.crypto_quantity,2)

        return value

    # gets and returns the value of UpdatePortfolio objects total value change
    def get_change(self):
        change = round(float(self.get_value()) - float(self.amount_usd),2)
        return change
