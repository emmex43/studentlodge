from django.urls import path
from . import views

app_name = 'housing'

urlpatterns = [
    path('contact/', views.contact_view, name='contact'),
    path('', views.home_feed, name='home_feed'),
    path('house/<int:id>/', views.house_detail, name='house_detail'),
    path('subscribe/', views.subscribe_view, name='subscribe'),
    path('toggle-save/<int:house_id>/', views.toggle_save_listing, name='toggle_save'),
    path('saved/', views.saved_listings_view, name='saved_listings'),
]
