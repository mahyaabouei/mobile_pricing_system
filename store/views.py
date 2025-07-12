from .models import Camera , Picture , Product , Order
from .serializers import CameraSerializer , PictureSerializer , ProductSerializer , OrderSerializer
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny , IsAuthenticated
import datetime

class CameraViewSet(APIView):
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
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
    def post (self,request):
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
        product = Product.objects.filter(id=id).first()
        if not product :
            return Response({"error":"Product not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    def delete (self,request,id):
        product = Product.objects.filter(id=id).first()
        if not product :
            return Response({"error":"Product not found"},status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response("product deleted",status=status.HTTP_200_OK)


class OrderViewSet(APIView):
    permission_classes = [IsAuthenticated]
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
        order = Order.objects.filter(id=id).first()
        if not order :
            return Response({"error":"Order not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
