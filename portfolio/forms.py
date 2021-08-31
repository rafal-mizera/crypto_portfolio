from django.forms import ModelForm
from .models import Portfolio,UpdatePortfolio
from django.contrib.auth import get_user_model

user = get_user_model()


class PortfolioForm(ModelForm):
    class Meta:
        model = Portfolio
        fields = ['name']


class UpdatePortfolioForm(ModelForm):
    class Meta:
        model = UpdatePortfolio
        fields = ['crypto','amount_usd']
