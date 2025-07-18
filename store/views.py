from .models import Camera , Picture , Product , Order
from .serializers import CameraSerializer , PictureSerializer , ProductSerializer , OrderSerializer
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny , IsAuthenticated
import datetime
from drf_spectacular.utils import extend_schema
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import CameraInputSerializer , PictureInputSerializer , ProductInputSerializer , OrderInputSerializer

class CameraViewSet(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    @extend_schema(request=CameraInputSerializer)
    def post (self,request):
        serializer = CameraSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    
    def get (self, request,id=None):
        if id :
            camera = Camera.objects.get(id=id)
            serializer = CameraSerializer(camera)
            return Response(serializer.data)
        else:
            cameras = Camera.objects.all()
            serializer = CameraSerializer(cameras,many=True)
            return Response(serializer.data)



class PictureViewSet(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]
    
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

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    @extend_schema(request=ProductInputSerializer)
    def post (self,request):
        if not request.user.has_perm('store.can_create_products'):
            return Response({"error":"You are not allowed to create products"},status=status.HTTP_403_FORBIDDEN)
        request.data['seller'] = request.user.id
        serializer = ProductSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get (self, request,id=None):
        if id :
            product = Product.objects.get(id=id)
            serializer = ProductSerializer(product)
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
        product = Product.objects.filter(id=request.data['product']).first()
        if not product :
            return Response({"error":"Product not found"},status=status.HTTP_404_NOT_FOUND)
        seller = product.seller
        buyer = request.user
        order = Order.objects.create(
            seller =seller,
            buyer = buyer,
            product = product ,
            status = 'ordering',
            sell_date = datetime.now()
        )
        serializer = OrderSerializer(order)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
    
    def get (self, request,id=None):
        if id :
            order = Order.objects.get(id=id)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        else:
            orders = Order.objects.all()
            serializer = OrderSerializer(orders,many=True)
            return Response(serializer.data)
        

    def patch (self,request,id):
        if not request.user.has_perm('store.can_update_order'):
            return Response({"error":"You are not allowed to update order"},status=status.HTTP_403_FORBIDDEN)
        order = Order.objects.filter(id=id).first()
        if not order :
            return Response({"error":"Order not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
