from rest_framework import serializers
from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'description')
        ordering = ['-id']



class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ('id', 'quantity', 'price', 'product')
        ordering = ['-id']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ('id', 'address', 'positions')
        ordering = ['-id']

    def create(self, validated_data):
        stock = Stock.objects.create(address=validated_data['address'])
        positions = validated_data.get('positions')

        for position in positions:
            StockProduct.objects.create(
                stock=stock,
                product=position['product'],
                quantity=position['quantity'],
                price=position['price'],
            )

        return stock

    def update(self, instance, validated_data):
        positions = validated_data.get('positions')
        for position in positions:
            StockProduct.objects.update_or_create(
                stock=instance,
                product=position['product'],
                defaults={'quantity': position['quantity'], 'price': position['price']})

        return instance

class StockViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ('id', 'address')
        ordering = ['-id']