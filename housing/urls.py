from django.urls import path
from . import views

app_name = 'housing'

urlpatterns = [
    path('contact/', views.contact_view, name='contact'),
    path('', views.home_feed, name='home_feed'),
    path('house/<int:id>/', views.house_detail, name='house_detail'),
    path('subscribe/', views.subscribe_view, name='subscribe'),
]
