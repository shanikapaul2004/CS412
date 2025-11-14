from django.urls import path
from .views import *

urlpatterns = [
    # Web views
    path('', random_view, name='index'),
    path('random', random_view, name='random'),
    path('jokes', all_jokes, name='all_jokes'),
    path('joke/<int:pk>', JokeDetailView.as_view(), name='joke_detail'),
    path('pictures', all_pictures, name='all_pictures'),
    path('picture/<int:pk>', PictureDetailView.as_view(), name='picture_detail'),
    
    # API endpoints
    path('api/', random_joke_api, name='api_random_joke'),
    path('api/random', random_joke_api, name='api_random_joke_alt'),
    path('api/jokes', JokeListAPIView.as_view(), name='api_jokes'),
    path('api/joke/<int:pk>', JokeDetailAPIView.as_view(), name='api_joke_detail'),
    path('api/pictures', PictureListAPIView.as_view(), name='api_pictures'),
    path('api/picture/<int:pk>', PictureDetailAPIView.as_view(), name='api_picture_detail'),
    path('api/random_picture', random_picture_api, name='api_random_picture'),
]