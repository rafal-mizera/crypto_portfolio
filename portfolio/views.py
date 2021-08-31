import requests
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Crypto,Portfolio,UpdatePortfolio
from .forms import PortfolioForm,UpdatePortfolioForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

def welcome(request):
    CURRENCIES = ["bitcoin","ethereum","tether","cardano","dogecoin","polkadot","ripple","solana","litecoin"]
    try:
        for item in CURRENCIES:
            res = requests.get(
                f"https://api.coingecko.com/api/v3/simple/price?ids={item}&vs_currencies=usd&include_24hr_change=true")
            rate = res.json()[f"{item}"]["usd"]
            change = round(res.json()[f"{item}"]["usd_24h_change"],2)
            obj = Crypto.objects.get(name=item)
            obj.rate = rate
            obj.change = change
            obj.save(update_fields=['rate','change'])
    except Crypto.DoesNotExist:
        for item in CURRENCIES:
            res = requests.get(
                f"https://api.coingecko.com/api/v3/simple/price?ids={item}&vs_currencies=usd&include_24hr_change=true")
            rate = res.json()[f"{item}"]["usd"]
            change = round(res.json()[f"{item}"]["usd_24h_change"],2)
            crypto_data = Crypto.objects.create(name=item,rate=rate,change=change)
            crypto_data.save()

    all_crypto = Crypto.objects.all()

    return render(request,'portfolio/welcome.html',{'all_crypto': all_crypto})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username,password=raw_password)
            login(request,user)
            return redirect("portfolio:welcome")
    else:
        form = UserCreationForm()

    return render(request,'portfolio/signup.html',{'form': form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.info(request,f"You are now logged in as {username}.")
                return redirect("portfolio:welcome")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()

    return render(request=request,template_name="portfolio/login.html",context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request,"You have successfully logged out.")
    return redirect("portfolio:welcome")


def details(request,name):
    try:
        portfolio = Portfolio.objects.get(name=name)
        updates = UpdatePortfolio.objects.filter(portfolio=portfolio)
        cryptos = set(item.crypto.name for item in updates)
        return render(request,'portfolio/details.html',{"updates": updates,'portfolio': portfolio,'cryptos': cryptos})

    except ObjectDoesNotExist:

        return render(request,'portfolio/not_found.html',{})


def create_portfolio(request):
    if request.method == "POST":
        form = PortfolioForm(request.POST)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user = request.user
            portfolio.save()
            return redirect('portfolio:user_portfolios')
    else:
        form = PortfolioForm()

    return render(request,'portfolio/create_portfolio.html',{'form': form})


def user_portfolios(request):
    user = request.user
    portfolios = Portfolio.objects.filter(user=user.id)
    return render(request,'portfolio/user_portfolios.html',{'portfolios': portfolios})


def update_portfolio(request,name):
    if request.method == "POST":
        portfolio = get_object_or_404(Portfolio,name=name)
        form = UpdatePortfolioForm(request.POST)
        if form.is_valid():
            update = form.save()
            update.portfolio = portfolio
            update.crypto_quantity += update.amount_usd / update.crypto.rate
            portfolio.save()
            update.save()
            return redirect('portfolio:details',portfolio)
    else:
        form = UpdatePortfolioForm()

    return render(request,'portfolio/update_portfolio.html',{'form': form,'name': name})


def delete_portfolio(self,name):
    portfolio = Portfolio.objects.get(name=name)
    portfolio.delete()

    return redirect('portfolio:user_portfolios')


def delete_position(id):
    position = get_object_or_404(UpdatePortfolio,pk=id)
    position.delete()
    portfolio = position.portfolio.name
    return redirect('portfolio:details',portfolio)
