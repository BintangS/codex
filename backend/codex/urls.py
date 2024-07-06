"""
URL configuration for codex project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from app import views
from . import socketHandler


urlpatterns = [
    path('', views.heatmap_view, name='heatmap_view'),
    path('test/', views.test_page_view, name='test_page_view'),
    path('sessions/', views.list_sessions, name='list_sessions'),
    path('sessions/<str:session_id>/', views.get_heatmap_data, name='get_heatmap_data'),
    path('sessions/<str:session_id>/delete/', views.delete_session, name='delete_session'),
    path('admin/', admin.site.urls),
    path('api/prompt', views.simple_chat_bot_view, name='simpleChatbotView'),
    path('api/prompt-history', views.simple_chat_bot_with_history_view, name='simpleChatbotWithHistoryView'),
]