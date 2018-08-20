from .models import Store, Product
from rest_framework import serializers, pagination

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('name', 'logo', 'address', 'status', 'category', 'id', 'owner')
        read_only_fields=('owner',)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields =('name','price', 'quantity','store','thumbnail',)
        #read_only_fields=('store',)




