from django.urls import path
from . import views

app_name = 'housing'

urlpatterns = [
    # The empty string '' means this is the homepage of the housing app
    path('', views.home_feed, name='home_feed'),
    path('house/<int:id>/', views.house_detail, name='house_detail'),
]
