from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status

# auth
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

# jwt
from rest_framework_simplejwt.tokens import RefreshToken

# model
from blog.models import BlogPost

# serializer
from blog.serializers import (PostSerializer, UserRegistrationSerializer, UserLoginSerializer)

# Authentication
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        print(user, 'registered')
        tokens = get_tokens_for_user(user)
        return Response({'tokens': tokens, "message": "User Successfully Created!"}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        print(user)
        if user:
            tokens = get_tokens_for_user(user)
            return Response({'tokens': tokens, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'non_field_errors': ['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
        

# CRUD
class Post(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        posts = BlogPost.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        request.data['author'] = request.user.id
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response("Post Added", status=status.HTTP_201_CREATED)
    
class SpecificPost(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        post = BlogPost.objects.filter(id=id).first()
        if post:
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("No Such Post", status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, id):
        post = BlogPost.objects.filter(id=id, author=request.user.id).first()
        if post:
            serializer = PostSerializer(post, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response("Post Updated", status=status.HTTP_200_OK)
        return Response("No Such Post", status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, id):
        post = BlogPost.objects.filter(id=id, author=request.user.id).first()
        if post:
            serializer = PostSerializer(post, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response("Post Updated", status=status.HTTP_200_OK)
        return Response("No Such Post", status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, id):
        post = BlogPost.objects.filter(id=id).first()
        if post:
            post.delete()
            return Response("Post Deleted", status=status.HTTP_200_OK)
        return Response("No Such Post", status=status.HTTP_404_NOT_FOUND)