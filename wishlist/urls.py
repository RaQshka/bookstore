from django.urls import path
from . import views
app_name = 'wishlist'

urlpatterns = [
    path('add_from_search/', views.add_from_search, name='add_from_search'),
    path('', views.wishlist_list, name='list'),
    path('edit/<int:pk>/', views.edit_wishlist, name='edit'),
    path('delete/<int:pk>/', views.delete_wishlist, name='delete'),
]