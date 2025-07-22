from django.urls import path
from .views import CameraViewSet,PictureViewSet,ProductViewSet,OrderViewSet,StatisticViewSet

urlpatterns = [
        path('camera/',CameraViewSet.as_view(),name='camera'),
        path('camera/<int:id>/',CameraViewSet.as_view(),name='camera'),
        path('picture/',PictureViewSet.as_view(),name='picture'),
        path('picture/<int:id>/',PictureViewSet.as_view(),name='picture'),
        path('product/' , ProductViewSet.as_view(), name='product'),
        path('product/<int:id>/' , ProductViewSet.as_view(), name='product'),
        path('order/' , OrderViewSet.as_view(), name='order'),
        path('order/<int:id>/' , OrderViewSet.as_view(), name='order'),
        path('statistic/' , StatisticViewSet.as_view(), name='statistic'),
    ]