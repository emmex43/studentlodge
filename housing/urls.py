from django.urls import path
from . import views

urlpatterns = [
    # The empty string '' means this is the homepage of the housing app
    path('', views.home_feed, name='home'),
]
