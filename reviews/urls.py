from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('listing/<int:listing_id>/review/', views.submit_review, name='submit_review'),
]