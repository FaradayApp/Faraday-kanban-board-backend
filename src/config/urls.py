from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from config import settings


api_urls = [
    path('', include(('users.urls', 'users'))),
    path('board/', include(('kanban_board.urls', 'kanban_board'))),
]

swagger_urls = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urls = api_urls + swagger_urls

urlpatterns = [
    path('v0/api/', include(urls)),
]
