from .models import Picture , Product , Order , ModelMobile
from .serializers import PictureSerializer , ProductSerializer , OrderSerializer , MobileSerializer
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny , IsAuthenticated
import datetime
from drf_spectacular.utils import extend_schema
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import PictureInputSerializer , ProductInputSerializer , OrderInputSerializer , ProductDetailSerializer
from django.db.models import Sum

class PictureViewSet(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @extend_schema(request=PictureInputSerializer)
    def post (self,request):
        serializer = PictureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def get (self, request,id=None):
        if id :
            picture = Picture.objects.get(id=id)
            serializer = PictureSerializer(picture)
            return Response(serializer.data)
        else:
            pictures = Picture.objects.all()
            serializer = PictureSerializer(pictures,many=True)
            return Response(serializer.data)


class ProductViewSet(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(request=ProductInputSerializer)
    def post (self,request):
        request.data['seller'] = request.user.id
        print(request.data)
        request.data['register_date'] = datetime.datetime.strptime(request.data['register_date'], '%Y-%m-%d') if request.data['register_date'] else None
        request.data['status_product'] = 'open' if request.data['status_product'] is None else request.data['status_product']
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def get (self, request,id=None):
        if id :
            product = Product.objects.get(id=id)
            serializer = ProductDetailSerializer(product)
            return Response(serializer.data)
        else:
            products = Product.objects.all()
            serializer = ProductSerializer(products,many=True)
            return Response(serializer.data)


    def patch (self,request,id):
        if not request.user.has_perm('store.can_update_products'):
            return Response({"error":"You are not allowed to update products"},status=status.HTTP_403_FORBIDDEN)
        product = Product.objects.filter(id=id).first()
        if not product :
            return Response({"error":"Product not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def delete (self,request,id):
        if not request.user.has_perm('store.can_delete_products'):
            return Response({"error":"You are not allowed to delete products"},status=status.HTTP_403_FORBIDDEN)
        product = Product.objects.filter(id=id).first()
        if not product :
            return Response({"error":"Product not found"},status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response("product deleted",status=status.HTTP_200_OK)


class OrderViewSet(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(request=OrderInputSerializer)
    def post (self,request):
        product_id = request.data.get('product')
        product = Product.objects.filter(id=int(product_id),status_product__in =['open','ordering']).first()
        if not product :
            return Response({"message":"محصول یافت نشد"},status=status.HTTP_404_NOT_FOUND)
        if product.seller == request.user :
            return Response({"message":"شما نمیتوانید خود را سفارش دهید"},status=status.HTTP_400_BAD_REQUEST)
        seller = product.seller
        buyer = request.user
        order = Order.objects.create(
            seller =seller,
            buyer = buyer,
            product = product ,
            status = 'ordering',
            sell_date = datetime.datetime.now()
        )
        serializer = OrderSerializer(order)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def get (self, request,id=None):
        if id :
            order = Order.objects.filter(Q(id=id) & (Q(buyer=request.user) | Q(seller=request.user))).first()
            if not order :
                return Response({"message":"سفارشی یافت نشد"},status=status.HTTP_404_NOT_FOUND)

            serializer = OrderSerializer(order)
            return Response(serializer.data)
        else:
            orders = Order.objects.filter(Q(buyer=request.user) | Q(seller=request.user))
            serializer = OrderSerializer(orders,many=True)
            return Response(serializer.data)


    def patch (self,request,id):
        if not id:
            return Response({"message":"شناسه سفارش را وارد کنید"},status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.filter(id=id).first()
        if not order :
            return Response({"message":"سفارش یافت نشد"},status=status.HTTP_404_NOT_FOUND)
        if order.seller != request.user :
            return Response({"message":"شما نمیتوانید این سفارش را بروزرسانی کنید"},status=status.HTTP_403_FORBIDDEN)
        serializer = OrderSerializer(order,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class StatisticViewSet(APIView):
    permission_classes = [IsAuthenticated]
    def get (self,request):
        orders_seller = Order.objects.filter(seller=request.user).count()
        orders_buyer = Order.objects.filter(buyer=request.user).count()
        products = Product.objects.filter(seller=request.user).count()
        total_price_seller = Order.objects.filter(seller=request.user,status='approved').aggregate(total_price=Sum('product__price'))['total_price'] or 0
        total_price_buyer = Order.objects.filter(buyer=request.user,status='approved').aggregate(total_price=Sum('product__price'))['total_price'] or 0
        return Response({"orders_seller":orders_seller,"orders_buyer":orders_buyer,"products":products,"total_price_seller":total_price_seller,"total_price_buyer":total_price_buyer})


# class MobileViewSet(APIView):
#     permission_classes = [IsAuthenticated]
#     def get (self,request):
#         mobiles = Mobile.objects.all()
#         serializer = MobileSerializer(mobiles,many=True)
#         return Response(serializer.data , status=status.HTTP_200_OK)

#     def post (self,request):
#         data = request.data
#         if request.data.get('is_apple'):
#             data['brand'] = 'apple'
#         else:
#             data['brand'] = request.data.get('brand')

#         serializer = MobileSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data , status=status.HTTP_201_CREATED)
#         return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
