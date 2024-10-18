from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    ActivityViewSet,
    WorkoutPlanViewSet,
    DietLogViewSet,
    RegisterView,
    CustomAuthToken,
    DietLogListCreateView,
    ProgressView,
    UserActivityHistoryView
)

# Router for ViewSets
router = DefaultRouter()
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'workout-plans', WorkoutPlanViewSet, basename='workout-plan')
router.register(r'diet-logs', DietLogViewSet, basename='diet-log')

# URL patterns
urlpatterns = [
    # Authentication and registration
    path('register/', RegisterView.as_view(), name='register'),
    
    # Use JWT for login
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT login endpoint
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT refresh endpoint

    # Include the router-generated URLs for activities, workout plans, and diet logs
    path('', include(router.urls)),

    # Detailed activity, workout plan, and diet log URLs
    path('activities/<int:pk>/', ActivityViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='activity-detail'),
    path('workout-plans/<int:pk>/', WorkoutPlanViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='workout-plan-detail'),
    path('diet-logs/<int:pk>/', DietLogViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='diet-log-detail'),

    # Diet log list and creation, progress view, and user activity history view
    path('diet/', DietLogListCreateView.as_view(), name='diet-log-list-create'),
    path('progress/', ProgressView.as_view(), name='progress'),

    # New endpoint for user activity history with optional filters.
    path('activities/history/', UserActivityHistoryView.as_view(), name='user-activity-history'),
]
