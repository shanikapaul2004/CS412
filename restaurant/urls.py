from django.urls import path 
from django.conf import settings
from . import views 

# url patterns specific to this app 

urlpatterns = [
    path(r'', views.main, name="main"),  # Root URL uses home view
    path(r'order/', views.order, name="order"),  # Quote page  
    path(r'confirmation/', views.confirmation, name="confirmation"),
]