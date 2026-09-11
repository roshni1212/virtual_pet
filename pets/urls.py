from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_pet, name='create_pet'),
    path('pet/<int:pet_id>/', views.dashboard, name='dashboard'),
    path('pet/<int:pet_id>/feed/', views.feed_pet, name='feed_pet'),
    path('pet/<int:pet_id>/play/', views.play_pet, name='play_pet'),
    path('pet/<int:pet_id>/sleep/', views.sleep_pet, name='sleep_pet'),
    path('pet/<int:pet_id>/pet/', views.pet_pet, name='pet_pet'),
    path('pet/<int:pet_id>/shop/', views.shop, name='shop'),
    path('pet/<int:pet_id>/shop/buy/<int:item_id>/', views.buy_item, name='buy_item'),
    path('pet/<int:pet_id>/game/', views.mini_game, name='mini_game'),
]