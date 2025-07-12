from rest_framework import serializers
from .models import Product , Order , Camera , Picture
from user.serializers import UserSerializer


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = '__all__'
 
class ProductSerializer(serializers.ModelSerializer):
    picture = PictureSerializer()
    camera = CameraSerializer()
    class Meta:
        model = Product
        fields = ['camera' , 'picture' , 'name' ,'seller','price' , 'description' , 'id' , 'created_at' , 'updated_at' , 'brand' , 'color' , 'type_product' 
                  , 'technical_problem' , 'hit_product' , 'registered' ,'register_date', 'guarantor' , 'repaired' , 'status_product' ]

class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    buyer = UserSerializer()
    seller = UserSerializer()
    class Meta:
        model = Order
        fields = ['product' , 'buyer' , 'seller' , 'sell_date' , 'status' , 'id' , 'created_at' , 'updated_at' ]