from django.urls import path
from . import views

app_name = "portfolio"
urlpatterns = [
    path(r'welcome',views.welcome,name='welcome'),
    path(r'details/<name>',views.details,name='details'),
    path(r'signup',views.signup,name='signup'),
    path(r'login',views.login_request,name='login_request'),
    path(r'logout',views.logout_request,name='logout_request'),
    path(r'create',views.create_portfolio,name='create_portfolio'),
    path(r'user_portfolios',views.user_portfolios,name='user_portfolios'),
    path(r'update_portfolio/<name>',views.update_portfolio,name='update_portfolio'),
    path(r'delete_portfolio/<name>',views.delete_portfolio,name='delete_portfolio'),
    path(r'delete_position/<id>',views.delete_position,name='delete_position'),
]
