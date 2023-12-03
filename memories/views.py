from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from knox.models import AuthToken
from .serializers import *
from .models import *
from django.db.models import Q
import json
from django.http import HttpResponse, JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


# Create your views here.

@api_view(['GET','POST'])
def register(request):
    if request.method == 'GET':
        shipments = User.objects.all()
        serializer = RegisterSerializer(shipments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "successfully registered"
            data['email'] = user.email
            data['username'] = user.username
            token = AuthToken.objects.create(user)[1]
            data['token'] = token
            data['password'] = user.password
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.validated_data
            data['username'] = user.username
            data['password'] = user.password
            token = AuthToken.objects.create(user)[1]
            data['token'] = token
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def changePassword(request):

    if request.method == 'PUT':

        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not request.user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            elif serializer.data.get("old_password") == serializer.data.get("new_password"):
                return Response({"old_password": ["new password cannot be same"]}, status=status.HTTP_400_BAD_REQUEST)
            request.user.set_password(serializer.data.get("new_password"))
            request.user.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def deletetokens(request):
    try:
        AuthToken.objects.all().delete()
        return Response(status=status.HTTP_201_CREATED)
    except AuthToken.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)



@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def memory(request):
    if request.method == 'GET':
        shipments = CreateMemory.objects.all()
        serializer = CreateMemorySerializer(shipments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CreateMemorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


