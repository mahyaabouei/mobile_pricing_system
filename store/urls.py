from django.urls import path
from .views import PictureViewSet,ProductViewSet,OrderViewSet,StatisticViewSet, ModelMobileViewSet, PardNumberViewSet

urlpatterns = [
        path('picture/',PictureViewSet.as_view(),name='picture'),
        path('picture/<int:id>/',PictureViewSet.as_view(),name='picture'),
        path('modelmobile/',ModelMobileViewSet.as_view(),name='modelmobile'),
        path('product/' , ProductViewSet.as_view(), name='product'),
        path('product/<int:id>/' , ProductViewSet.as_view(), name='product'),
        path('order/' , OrderViewSet.as_view(), name='order'),
        path('order/<int:id>/' , OrderViewSet.as_view(), name='order'),
        path('statistic/' , StatisticViewSet.as_view(), name='statistic'),
        path('pardnumber/' , PardNumberViewSet.as_view(), name='pardnumber'),
    ]