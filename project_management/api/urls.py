from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import 
from . import views
# router = DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'projects', ProjectViewSet)
# router.register(r'project-members', ProjectMemberViewSet)
# router.register(r'tasks', TaskViewSet)
# router.register(r'comments', CommentViewSet)

urlpatterns = [
    # path('api/users/register/', views.user_view, name='user-register'),  # POST for registration
    # path('api/users/login/', views.user_view, name='user-login'),        # POST for login
    path('api/users/<int:pk>/', views.user_view, name='user-detail'),


    # Project Endpoints
    path('api/projects/', views.project_view, name='project-list-create'),
    path('api/projects/<int:pk>/', views.project_update_delete_view, name='project-detail-update-delete'),

    # Task Endpoints
    path('api/projects/<int:project_id>/tasks/', views.task_view, name='task-list-create'),
    path('api/tasks/<int:pk>/', views.task_update_delete_view, name='task-detail-update-delete'),

    # Comment Endpoints
    path('api/tasks/<int:task_id>/comments/', views.comment_view, name='comment-list-create'),
    path('api/comments/<int:pk>/', views.comment_update_delete_view, name='comment-detail-update-delete'),
    path('api/users/register/', views.RegisterUserView.as_view(), name='user-register'),
    path('api/users/login/', views.LoginUserView.as_view(), name='user-login'),
    # path('api/users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    # path('api/projects/', ProjectViewSet.as_view({'get': 'list', 'post': 'create'}), name='project-list-create'),
    # path('api/projects/<int:pk>/', ProjectViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='project-detail-update-delete'),
    # path('api/projects/<int:project_id>/tasks/', TaskViewSet.as_view({'get': 'list', 'post': 'create'}), name='task-list-create'),
    # path('api/tasks/<int:pk>/', TaskViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='task-detail-update-delete'),
    # path('api/tasks/<int:task_id>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comment-list-create'),
    # path('api/comments/<int:pk>/', CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='comment-detail-update-delete'),

]
