from django.urls import path 
from django.conf import settings
from . import views 

# url patterns specific to this app 

urlpatterns = [
    path('', views.home, name="home"),  # Root URL uses home view
    path('quote/', views.quote, name="quote"),  # Quote page  
    path('show_all/', views.show_all, name="show_all"),
    path('about/', views.about, name="about"),
]