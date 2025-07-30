from rest_framework import serializers
from .models import Product , Order , Picture , ModelMobile, Color
from user.serializers import UserSerializer

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    picture = serializers.PrimaryKeyRelatedField(queryset=Picture.objects.all(), many=True)

    class Meta:
        model = Product
        fields = ['picture' , 'name' ,'seller','price' , 'description' , 'id' , 'created_at' , 'updated_at' , 'color' , 'type_product'
                  , 'technical_problem' , 'hit_product' , 'guarantor' , 'repaired' , 'status_product' ]

class ProductDetailSerializer(serializers.ModelSerializer):
    picture = PictureSerializer(many=True)

    class Meta:
        model = Product
        fields = ['camera' , 'picture' , 'name' ,'seller','price' , 'description' , 'id' , 'created_at' , 'updated_at' , 'color' , 'type_product'
                  , 'technical_problem' , 'hit_product' , 'guarantor' , 'repaired' , 'status_product' ]


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    buyer = UserSerializer()
    seller = UserSerializer()
    class Meta:
        model = Order
        fields = ['product' , 'buyer' , 'seller' , 'sell_date' , 'status' , 'id' , 'created_at' , 'updated_at' ]

class PictureInputSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)
    file = serializers.FileField(required=False, allow_null=True)

class ProductInputSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    color = serializers.CharField(required=False, allow_blank=True)
    type_product = serializers.CharField(required=False, allow_blank=True)
    technical_problem = serializers.CharField(required=False, allow_blank=True)
    hit_product = serializers.BooleanField(required=False)
    guarantor = serializers.CharField(required=False, allow_blank=True)
    repaired = serializers.BooleanField(required=False)
    status_product = serializers.CharField(required=False, allow_blank=True)
    picture = PictureInputSerializer(required=False)

class OrderInputSerializer(serializers.Serializer):
    product = ProductInputSerializer(required=False)
    buyer = UserSerializer(required=False)
    seller = UserSerializer(required=False)
    sell_date = serializers.DateField(required=False, allow_null=True)
    status = serializers.CharField(required=False, allow_blank=True)


class MobileInputSerializer(serializers.Serializer):
    model_name = serializers.CharField(required=False, allow_blank=True)
    color = serializers.CharField(required=False, allow_blank=True)
    picture = PictureInputSerializer(required=False)
    is_apple = serializers.BooleanField(required=False)
    part_number = serializers.CharField(required=False, allow_blank=True)
    registered = serializers.BooleanField(required=False)
    link = serializers.URLField(required=False, allow_blank=True)


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name', 'hex_code']

class MobileSerializer(serializers.ModelSerializer):
    picture = PictureSerializer(many=True)
    colors = ColorSerializer(many=True, read_only=True)

    class Meta:
        model = ModelMobile
        fields = "__all__"
