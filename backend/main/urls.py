from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .views import UserProfileView, DeleteAccountView



urlpatterns = [
    path('', views.hello),
    path('api/', views.api),
    path('api/constructions/', views.construction_list),
    path('signup/', views.signup_view), #Sign Up page
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', views.logout_view),
    path('api/verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/delete-account/', DeleteAccountView.as_view(), name='delete-account'),
]