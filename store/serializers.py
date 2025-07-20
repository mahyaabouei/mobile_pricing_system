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
    camera = serializers.PrimaryKeyRelatedField(queryset=Camera.objects.all(), many=True)
    picture = serializers.PrimaryKeyRelatedField(queryset=Picture.objects.all(), many=True)

    class Meta:
        model = Product
        fields = ['camera' , 'picture' , 'name' ,'seller','price' , 'description' , 'id' , 'created_at' , 'updated_at' , 'brand' , 'color' , 'type_product' 
                  , 'technical_problem' , 'hit_product' , 'registered' ,'register_date', 'guarantor' , 'repaired' , 'status_product' ]

class ProductDetailSerializer(serializers.ModelSerializer):
    camera = CameraSerializer(many=True)
    picture = PictureSerializer(many=True)
    
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


class CameraInputSerializer(serializers.Serializer):
    name = serializers.CharField(required=True , allow_blank=True)
    resolution = serializers.CharField(required=True , allow_blank=True)


class PictureInputSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)
    file = serializers.FileField(required=False, allow_null=True)

class ProductInputSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    brand = serializers.CharField(required=False, allow_blank=True)
    color = serializers.CharField(required=False, allow_blank=True)
    type_product = serializers.CharField(required=False, allow_blank=True)
    technical_problem = serializers.CharField(required=False, allow_blank=True)
    hit_product = serializers.BooleanField(required=False)
    registered = serializers.BooleanField(required=False)
    register_date = serializers.DateField(required=False, allow_null=True)
    guarantor = serializers.CharField(required=False, allow_blank=True)
    repaired = serializers.BooleanField(required=False)
    status_product = serializers.CharField(required=False, allow_blank=True)
    camera = CameraInputSerializer(required=False)
    picture = PictureInputSerializer(required=False)

class OrderInputSerializer(serializers.Serializer):
    product = ProductInputSerializer(required=False)
    buyer = UserSerializer(required=False)
    seller = UserSerializer(required=False)
    sell_date = serializers.DateField(required=False, allow_null=True)
    status = serializers.CharField(required=False, allow_blank=True)
