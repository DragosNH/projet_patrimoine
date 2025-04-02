# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Construction
from .serializers import ConstructionSerializer, SignUpSerializer
from . import serializers


def hello(request):
    return HttpResponse("Hello world!")

@api_view(['GET'])
def api(request):
    return Response({"message": "Welcome to the api"})

@api_view(['GET'])
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