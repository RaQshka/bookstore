from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('start/<int:listing_id>/', views.start_chat, name='start_chat'),
    path('list/', views.chat_list, name='chat_list'),
    path('<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('notifications/', views.notifications, name='notifications'),
]