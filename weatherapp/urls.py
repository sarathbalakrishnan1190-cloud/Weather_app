from django.urls import path
from .views import WeatherAPI, OutfitAPI, weather_page, outfit_check_page

urlpatterns = [
    
    path('', weather_page, name='weather_page'),
    path('outfit-check/', outfit_check_page, name='outfit_check_page'),

    
    path('api/weather/', WeatherAPI.as_view(), name='weather_api'),
    path('api/outfit/', OutfitAPI.as_view(), name='outfit_api'),
]
