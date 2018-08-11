from django.contrib import admin
from django.urls import path
from api_auth import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/login', views.login),
    path('api/account/signup', views.signup),
    path('api/account/detail', views.get_account_detail),
    path('api/account/send_eth', views.send_ether),
]