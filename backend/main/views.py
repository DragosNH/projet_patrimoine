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

def hello(request):
    return HttpResponse("Hello world!")

@api_view(['GET'])
def api(request):
    return Response({"message": "Welcome to the api"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def construction_list(request):
    constructions = Construction.objects.all()
    serializers = ConstructionSerializer(constructions, many=True)
    return Response(serializers.data)

@api_view(['POST'])
def signup_view(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Compte cr\u00e9\u00e9 avec succ\u00e8s"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "D\u00e9connexion r\u00e9ussie"}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

