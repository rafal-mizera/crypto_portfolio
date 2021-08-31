from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from . import models

admin.site.register(models.Portfolio)
admin.site.register(models.Crypto)
admin.site.register(models.UpdatePortfolio)