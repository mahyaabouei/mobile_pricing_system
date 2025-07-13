from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random
from .models import Otp , User
from utils.message import Message
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer


class OtpView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        mobile = request.data.get('mobile')
        if not mobile:
            return Response({'error': 'mobile is required'}, status=status.HTTP_400_BAD_REQUEST)
        otp = random.randint(100000, 999999)
        otp = Otp.objects.create(mobile=mobile, otp=otp)
        Message(otp,mobile).otpSMS()
        return Response({'message': 'OTP sent to mobile'}, status=status.HTTP_200_OK) 


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        mobile = request.data.get('mobile')
        otp = request.data.get('otp')
        if not mobile or not otp:
            return Response({'error': 'mobile and otp are required'}, status=status.HTTP_400_BAD_REQUEST)
        otp = Otp.objects.filter(mobile=mobile, otp=otp).first()
        if not otp:
            return Response({'error': 'invalid otp'}, status=status.HTTP_400_BAD_REQUEST)
        otp.delete()
        user = User.objects.filter(mobile=mobile).first()
        if not user:
            return Response({'error': 'user not registered'}, status=status.HTTP_404_NOT_FOUND)
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return Response({'access': access,'refresh': str(refresh)}, status=status.HTTP_200_OK)
    

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        mobile = request.data.get('mobile')
        otp = request.data.get('otp')
        if not mobile or not otp:
            return Response({'error': 'mobile and otp are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        otp = Otp.objects.filter(mobile=mobile, otp=otp).first()
        if not otp:
            return Response({'error': 'invalid otp'}, status=status.HTTP_400_BAD_REQUEST)
        otp.delete()

        if User.objects.filter(mobile=mobile).exists():
            return Response({'error': 'user with this mobile already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create(
            mobile=mobile,
            username = request.data.get('uniqidentifier'),
            uniqidentifier = request.data.get('uniqidentifier'),
            first_name = request.data.get('first_name'),
            last_name = request.data.get('last_name'),
            email = request.data.get('email'),
            company = request.data.get('company'),
            sheba_number = request.data.get('sheba_number'),
            card_number = request.data.get('card_number'),
            account_number = request.data.get('account_number'),
            account_bank = request.data.get('account_bank'),
            address = request.data.get('address'),
            city = request.data.get('city'),
            is_active = True,
        )
        serializer = UserSerializer(user)
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return Response({'access': access,'refresh': str(refresh)}, status=status.HTTP_200_OK)
    

class InformationUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get (self, request,id=None):
        user = request.user
        if id:
            user = User.objects.filter(id=id).first()
            if not user:
                return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
class UserUpdateView(APIView):
    permission_classes=[IsAuthenticated]
    def patch(self,request,id):
        user = User.objects.filter(id=id).first()
        if not user:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        is_verified =  request.data.get('is_verified')
        is_verified = user.is_verified
        user.save()
        return Response ({'success' : 'user updated'}, status=status.HTTP_200_OK)
    
        