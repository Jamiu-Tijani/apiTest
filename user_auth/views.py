from django.http.response import ResponseHeaders
from django.shortcuts import render
from .serializers import dataSerializer, userdataSerializer
from .models import userData
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate

# Create your views here.


class userReg(generics.GenericAPIView):
    serializer_class = dataSerializer
    queryset = userData.objects.all()
    def post(self, request):
            try:
                user =request.data
                username = user['username']
                email = user['email']
                password = user['password']
                if userData.objects.filter(username = username).exists() or userData.objects.filter(email=email).exists() :
                    context = {
                    'message':'username or email already exists'
                    }
                    return Response(context,status=status.HTTP_201_CREATED)
                else:
                    userData.objects.create_user(username, email,password)
                    userData.save
                    context = {
                    'message':'username registered successfully'
                    }
                    return Response(context,status=status.HTTP_201_CREATED)
            except Exception as e:
                    context = {
                        'message': e
                    }
                    return Response(context,status.HTTP_404_NOT_FOUND)

class username_change(generics.GenericAPIView):
    serializer_class = userdataSerializer
    def post(self, request):
        user = request.data
        username = user['username']
        password = user['password']
        new_username = user['new_username']
        print(username)

        auth = authenticate(username=username, password=password)
        print(auth)
        if auth is not None:
            u = userData.objects.get(username=username)
            u.username = new_username
            u.save()
            context = {
                'message': "username changed to "+ new_username
            }
            return Response(context,status=status.HTTP_201_CREATED )
        else:
            context = {
                'message': "username or password invalid"
            }
            return Response(context,status=status.HTTP_201_CREATED )