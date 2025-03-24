from rest_framework import serializers
from .models import Category, Product

class ProductSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset = Category.objects.all()
    )


    class Meta:
        model = Product
        fields = '__all__'