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
from .serializers import UserSerializer , OtpInputSerializer  , UserInputSerializer , LoginInputSerializer
from drf_spectacular.utils import extend_schema


class OtpView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(request=OtpInputSerializer,)
    def post(self, request):
        mobile = request.data.get('mobile')
        if not mobile:
            return Response({'message': 'شماره موبایل را وارد کنید'}, status=status.HTTP_400_BAD_REQUEST)
        otp = random.randint(100000, 999999)
        print(otp)
        otp = Otp.objects.create(mobile=mobile, otp=otp)
        Message(otp,mobile).otpSMS()
        return Response({'message': 'کد تایید به شماره موبایل شما ارسال شد'}, status=status.HTTP_200_OK) 


class LoginView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(request=LoginInputSerializer,)
    def post(self, request):
        mobile = request.data.get('mobile')
        otp = request.data.get('otp')
        if not mobile or not otp:
            return Response({'message': 'شماره موبایل و کد تایید را وارد کنید'}, status=status.HTTP_400_BAD_REQUEST)
        otp = Otp.objects.filter(mobile=mobile, otp=otp).first()
        if not otp:
            return Response({'message': 'کد تایید اشتباه است'}, status=status.HTTP_400_BAD_REQUEST)
        otp.delete()
        user = User.objects.filter(mobile=mobile).first()

        if not user:
            user = User.objects.create(
                mobile=mobile,
                username=mobile,
            )
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return Response({'access': access,'refresh': str(refresh)}, status=status.HTTP_200_OK)
    

class RegisterView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(request=UserInputSerializer)
    def post(self, request):
        user = request.user
        if user.is_register:
            return Response({'message': 'قبلا ثبت نام کردید'}, status=status.HTTP_400_BAD_REQUEST)
        User.objects.filter(id=user.id).update(
            mobile=request.data.get('mobile'),
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
            is_register = True,
        )

        return Response({'message': 'اطلاعات شما ثبت شد'}, status=status.HTTP_200_OK)
    

class InformationUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get (self, request,id=None):
        user = request.user
        if not user.admin:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
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
    @extend_schema(request=UserInputSerializer)
    def patch(self,request,id):
        user = User.objects.filter(id=id).first()
        if not user:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response ({'success' : 'user updated'}, status=status.HTTP_200_OK)
    

class RefreshView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        refresh = RefreshToken(request.data.get('refresh'))
        access = str(refresh.access_token)
        return Response({'access': access}, status=status.HTTP_200_OK)

