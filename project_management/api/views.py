from django.shortcuts import render
from rest_framework import viewsets
from .models import Project, ProjectMember, Task, Comment
from .serializers import UserSerializer, ProjectSerializer, ProjectMemberSerializer, TaskSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

# User Viewset
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.contrib.auth import get_user_model, authenticate
from rest_framework.permissions import IsAuthenticated
from .models import Project, Task, Comment
from .serializers import UserSerializer, ProjectSerializer, TaskSerializer, CommentSerializer

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_http_methods
from rest_framework.parsers import JSONParser
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
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            # Respond with success and include both access and refresh tokens
            return Response({
                'message': 'Login successful',
                'access_token': access_token,
                'refresh_token': refresh_token
            })

            # return Response({'message': 'Login successful'})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



# Project Views
@csrf_exempt
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
            return JsonResponse(
                {"message": "Project Created Successful", "data": serializer.data}, 
                status=201
            )
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
# @require_http_methods(["PUT", "PATCH", "DELETE"])
def project_update_delete_view(request, pk):
    try:
        project = Project.objects.get(id=pk)
    except Project.DoesNotExist:
        return JsonResponse({"error": "Project not found"}, status=404)
    if request.method == 'GET':
        if pk:
            project = Project.objects.get(id=pk)
            serializer = ProjectSerializer(project)
            return JsonResponse(serializer.data, safe=False)

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
@csrf_exempt
# @require_http_methods(["GET", "POST"])
def task_view(request, project_id=None, pk=None):
    if request.method == 'GET':
        if pk:  # Retrieve specific task by pk
            try:
                task = Task.objects.get(id=pk)
                serializer = TaskSerializer(task)
                return JsonResponse(serializer.data, safe=False)
            except Task.DoesNotExist:
                return JsonResponse({"error": "Task not found"}, status=404)
        
        # List all tasks for a project
        tasks = Task.objects.filter(project_id=project_id)
        serializer = TaskSerializer(tasks, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':  # Create a new task
        data = JSONParser().parse(request)
        
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return JsonResponse({"error": "Project not found"}, status=404)
        
        # Set the project ID explicitly before saving the task
        data['project'] = project.id
        
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # Save the task with the associated project
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
# @require_http_methods(["PUT", "PATCH", "DELETE"])
def task_update_delete_view(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)
    if request.method == 'GET':
        if pk:
            task = Task.objects.get(id=pk)
            serializer = TaskSerializer(task)
            return JsonResponse(serializer.data, safe=False)
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
@csrf_exempt
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


@csrf_exempt
# @require_http_methods(["PUT", "PATCH", "DELETE"])
def comment_update_delete_view(request, pk):
    try:
        comment = Comment.objects.get(id=pk)
    except Comment.DoesNotExist:
        return JsonResponse({"error": "Comment not found"}, status=404)
    if request.method == 'GET':
        if pk:
            comment = Comment.objects.get(id=pk)
            serializer = CommentSerializer(comment)
            return JsonResponse(serializer.data, safe=False)
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
@csrf_exempt
def user_view(request, pk=None):
    if request.method == 'GET':
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, safe=False)

    # For Update User (PUT/PATCH /api/users/{id}/)
    if request.method in ['PUT', 'PATCH']:
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        data = JSONParser().parse(request)
        serializer = UserSerializer(user, data=data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {"message": "Update Successful", "data": serializer.data}, 
                status=200
            )
        return JsonResponse(serializer.errors, status=400)

    # For Delete User (DELETE /api/users/{id}/)
    elif request.method == 'DELETE':
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        user.delete()
        return JsonResponse({"message": "User deleted successfully"}, status=204)

from rest_framework import viewsets
from .models import Project
from .serializers import ProjectSerializer
from rest_framework.permissions import IsAuthenticated

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        if project_id:
            return self.queryset.filter(project_id=project_id)
        return self.queryset
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        task_id = self.kwargs.get('task_id')
        if task_id:
            return self.queryset.filter(task_id=task_id)
        return self.queryset
