# -*- coding: utf-8 -*-
from token import tok_name
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Construction
from .serializers import ConstructionSerializer, SignUpSerializer
from . import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.conf import settings
from .utils import email_verification_token
from django.contrib.auth import get_user_model
from rest_framework.views import APIView

def hello(request):
    return HttpResponse("Hello world!")

@api_view(['GET'])
def api(request):
    return Response({"message": "Welcome to the api"})

# View info
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def construction_list(request):
    constructions = Construction.objects.all()
    serializers = ConstructionSerializer(constructions, many=True)
    return Response(serializers.data)

# Sign up
@api_view(['POST'])
def signup_view(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = email_verification_token.make_token(user)

        verify_url = f"http://127.0.0.1:8000/api/verify-email/{uid}/{token}/"

        send_mail(
            subject = "V\u00e9rification de votre adresse email",
            message=f"Cliquez sur ce lien pour v\u00e9rifier votre email : {verify_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        return Response({"message": "Compte cr\u00e9\u00e9 avec succ\u00e8s. V\u00e9rifiez votre e-mail pour activer votre compte."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Logout
@api_view(['POST'])
def logout_view(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "D\u00e9connexion r\u00e9ussie"}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

# Verify email
@api_view(['GET'])
def verify_email(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None 

    if user and email_verification_token.check_token(user, token):
        user.is_verified = True
        user.save()
        return Response(
            {"message": "Email v\u00e9rifi\u00e9 avec succ\u00e8s"},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"error": "Lien invalide ou expir\u00e9"},
            status=status.HTTP_400_BAD_REQUEST
        )


# Delete user
class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        password = request.data.get('password')
        user = request.user

        if not user.check_password(password):
            return Response({'error': "Le mot de passe n'est pas correct."}, status=400)

        user.delete()
        return Response({'message': 'Compte supprimé avec succès'}, status=200)