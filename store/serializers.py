from .models import Store
from rest_framework import serializers, pagination

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('name', 'logo', 'address', 'status', 'category', 'id', 'owner')
        read_only_fields=('owner',)



