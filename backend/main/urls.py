from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.tokens import PasswordResetTokenGenerator

urlpatterns = [
    path('', views.hello),
    path('api/', views.api),
    path('api/constructions/', views.construction_list),
    path('signup/', views.signup_view),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', views.logout_view),
    path('api/verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
]