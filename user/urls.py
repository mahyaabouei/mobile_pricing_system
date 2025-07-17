from django.urls import path
from .views import OtpView, LoginView, RegisterView, InformationUserView ,UserUpdateView, RefreshView, ProfileView

urlpatterns = [
    path('otp/', OtpView.as_view(), name='otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/',RegisterView.as_view(), name='register'),
    path('information/',InformationUserView.as_view(), name='information'),
    path('information/<int:id>/',InformationUserView.as_view(), name='information'),
    path('profile/',ProfileView.as_view(), name='profile'),
    path('update/<int:id>/',UserUpdateView.as_view(), name='update'),
    path('refresh/', RefreshView.as_view(), name='refresh'),

]