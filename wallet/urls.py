from django.contrib import admin
from django.urls import path
from api_auth import views
from store import views as store_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/login', views.login),
    path('api/account/signup', views.signup),
    path('api/account/detail', views.get_account_detail),
    path('api/account/send_eth', views.send_ether),
    path('api/transactions', views.get_transactions),
    path('api/get_address', views.get_address),
    path('api/stores', store_views.StoreListCreateView.as_view()),
    path('api/store/<int:pk>', store_views.StoreDetailUpdate.as_view()),
    path('api/get_user_store', store_views.get_user_store),

]