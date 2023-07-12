from django.urls import path, include

from users import views


auth_urls = [
    path('registration/', views.RegistrationUserAPI.as_view(), name='registration'),
    path('login/', views.LoginUserAPI.as_view(), name='login'),
    path('refresh/', views.RefreshTokenAPI.as_view(), name='refresh'),
]

users_urls = [
    path('information/', views.UserAPI.as_view(), name='user-information'),
]

urlpatterns = [
    path('auth/', include(auth_urls)),
    path('user/', include(users_urls)),
]
