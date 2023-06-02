from django.urls import path
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh

from server.apps.users import views

auth_patterns = [
    path('auth/login/', token_obtain_pair, name='login'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/signup/', views.RegisterView.as_view(), name='register'),
    path('auth/update_token/', token_refresh, name='update_token'),
]

user_patterns = [
    path('account/', views.UserViewSet.as_view(), name='account view'),
]


urlpatterns = auth_patterns + user_patterns
