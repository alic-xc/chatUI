from django.urls import path
from .views import *

urlpatterns = [
    path('account/login', LoginView.as_view(), name='login'),
    path('account/logout', logout, name='logout'),
    path('account/register', RegisterView.as_view(), name='register'),
    path('', DashboardView.as_view(), name='dashboard'),
    path('chat_room/<title>', ChatRoomView.as_view(), name='chat_room'),
    path('update_chat/<message_id>/', update_chat)
]

