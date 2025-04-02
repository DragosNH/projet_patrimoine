from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello),
    path('api/', views.api),
    path('api/constructions/', views.construction_list),
    path('signup/', views.signup_view),
]