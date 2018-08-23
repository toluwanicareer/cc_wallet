from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from django.contrib.auth.models import User
from web3.auto import w3, Web3
from api_auth.models import Wallet, Transaction
from .models import Store, Product, Cart
from django.conf import settings
from .serializers import StoreSerializer, ProductSerializer
from rest_framework import generics
import pdb

# Create your views here.

@csrf_exempt
@api_view(["GET"])
def get_user_store(request):
    try:
        store=Store.objects.get(owner=request.user)
    except Store.DoesNotExist:
        data={'message': 'Store not available', 'status':404}
        return Response(data, status=HTTP_404_NOT_FOUND)
    store_json=StoreSerializer(str).data
    data={'store':store_json, 'message':'successful', 'status':200}
    return Response(data, status=HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
def add_to_cart(request):
    object, created=Cart.objects.get_or_create(owner=request.user)
    data=request.data.get('product_id')
    quantity=request.get('qunatity')



class StoreListCreateView(generics.ListCreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    def perform_create(self,serializer):
        try:
            serializer.save(owner=self.request.user)
        except:
            self.object=None
            
class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self,*args, **kwargs):
        return Product.objects.filter(store__id=self.request.GET.get('id'))

    def perform_create(self, serializer):
        #pdb.set_trace()
        store=Store.objects.get(id=self.request.GET.get('id'))
        serializer.save(store=store)

    #def create(self, request, *args, **kwargs):


class StoreDetailUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer



class ProductDetailUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

























