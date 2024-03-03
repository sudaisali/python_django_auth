from django.urls import path 
from rest_framework_simplejwt import views as jwt_views 
from .views import *

urlpatterns = [
      path('registration/', SignUpView.as_view()), # post: username, email, password1, password2
      path('login/', LoginView.as_view()), # post: username, password
      path('refresh-token' , jwt_views.TokenRefreshView.as_view()), # refresh
      path('user/', AllUsers.as_view()),

]