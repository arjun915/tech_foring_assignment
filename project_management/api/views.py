from django.shortcuts import render
from rest_framework import viewsets
from .models import Project, ProjectMember, Task, Comment
from .serializers import UserSerializer, ProjectSerializer, ProjectMemberSerializer, TaskSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User


# User Viewset
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.contrib.auth import get_user_model, authenticate
from rest_framework.permissions import IsAuthenticated
from .models import Project, Task, Comment
from .serializers import UserSerializer, ProjectSerializer, TaskSerializer, CommentSerializer


# User Registration
class RegisterUserView(APIView):
    def post(self, request):
        data = request.data
        try:
            user = get_user_model().objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                first_name=data.get('first_name', ''),
                last_name=data.get('last_name', '')
            )
            return Response({'message': 'User created successfully!'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# # User Login
class LoginUserView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            # Authenticate user and create a token here (using session authentication)
            return Response({'message': 'Login successful'})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# # User Detail
# class UserDetailView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, pk):
#         try:
#             user = get_user_model().objects.get(pk=pk)
#             serializer = UserSerializer(user)
#             return Response(serializer.data)
#         except get_user_model().DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

#     def put(self, request, pk):
#         try:
#             user = get_user_model().objects.get(pk=pk)
#             serializer = UserSerializer(user, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except get_user_model().DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

#     def delete(self, request, pk):
#         try:
#             user = get_user_model().objects.get(pk=pk)
#             user.delete()
#             return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
#         except get_user_model().DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


# # Project Viewset
# class ProjectViewSet(viewsets.ModelViewSet):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)


# # Task Viewset
# class TaskViewSet(viewsets.ModelViewSet):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     permission_classes = [IsAuthenticated]


# # Comment Viewset
# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_http_methods
from rest_framework.parsers import JSONParser
# from .models import Project, Task, Comment
# from .serializers import ProjectSerializer, TaskSerializer, CommentSerializer

# Project Views
# @csrf_exempt
# @require_http_methods(["GET", "POST"])
def project_view(request, pk=None):
    if request.method == 'GET':
        if pk:
            project = Project.objects.get(id=pk)
            serializer = ProjectSerializer(project)
            return JsonResponse(serializer.data, safe=False)
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


# @csrf_exempt
# @require_http_methods(["PUT", "PATCH", "DELETE"])
def project_update_delete_view(request, pk):
    try:
        project = Project.objects.get(id=pk)
    except Project.DoesNotExist:
        return JsonResponse({"error": "Project not found"}, status=404)

    if request.method in ['PUT', 'PATCH']:
        data = JSONParser().parse(request)
        serializer = ProjectSerializer(project, data=data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        project.delete()
        return JsonResponse({"message": "Project deleted successfully"}, status=204)


# Task Views
# @csrf_exempt
# @require_http_methods(["GET", "POST"])
def task_view(request, project_id=None, pk=None):
    if request.method == 'GET':
        if pk:
            task = Task.objects.get(id=pk)
            serializer = TaskSerializer(task)
            return JsonResponse(serializer.data, safe=False)
        tasks = Task.objects.filter(project_id=project_id)
        serializer = TaskSerializer(tasks, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save(project_id=project_id)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


# @csrf_exempt
# @require_http_methods(["PUT", "PATCH", "DELETE"])
def task_update_delete_view(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)

    if request.method in ['PUT', 'PATCH']:
        data = JSONParser().parse(request)
        serializer = TaskSerializer(task, data=data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        task.delete()
        return JsonResponse({"message": "Task deleted successfully"}, status=204)


# Comment Views
# @csrf_exempt
# @require_http_methods(["GET", "POST"])
def comment_view(request, task_id=None, pk=None):
    if request.method == 'GET':
        if pk:
            comment = Comment.objects.get(id=pk)
            serializer = CommentSerializer(comment)
            return JsonResponse(serializer.data, safe=False)
        comments = Comment.objects.filter(task_id=task_id)
        serializer = CommentSerializer(comments, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(task_id=task_id)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


# @csrf_exempt
# @require_http_methods(["PUT", "PATCH", "DELETE"])
def comment_update_delete_view(request, pk):
    try:
        comment = Comment.objects.get(id=pk)
    except Comment.DoesNotExist:
        return JsonResponse({"error": "Comment not found"}, status=404)

    if request.method in ['PUT', 'PATCH']:
        data = JSONParser().parse(request)
        serializer = CommentSerializer(comment, data=data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        comment.delete()
        return JsonResponse({"message": "Comment deleted successfully"}, status=204)

def user_view(request, pk=None):
    # For Register User (POST /api/users/register/)
    if request.method == 'POST':
        if pk is None:  # Register user (no user id provided)
            data = JSONParser().parse(request)
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
                token = Token.objects.create(user=user)
                return JsonResponse({
                    "user": serializer.data,
                    "token": token.key
                }, status=201)
            return JsonResponse(serializer.errors, status=400)
        else:  # Login user (using existing user id)
            data = JSONParser().parse(request)
            username = data.get("username")
            password = data.get("password")
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    token, created = Token.objects.get_or_create(user=user)
                    return JsonResponse({
                        "token": token.key
                    }, status=200)
                else:
                    return JsonResponse({"error": "Invalid credentials"}, status=400)
            except User.DoesNotExist:
                return JsonResponse({"error": "User does not exist"}, status=404)

    # For Get User Details (GET /api/users/{id}/)
    elif request.method == 'GET':
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, safe=False)

    # For Update User (PUT/PATCH /api/users/{id}/)
    elif request.method in ['PUT', 'PATCH']:
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        data = JSONParser().parse(request)
        serializer = UserSerializer(user, data=data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

    # For Delete User (DELETE /api/users/{id}/)
    elif request.method == 'DELETE':
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        user.delete()
        return JsonResponse({"message": "User deleted successfully"}, status=204)