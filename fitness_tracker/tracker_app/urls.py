from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet, WorkoutPlanViewSet, DietLogViewSet, RegisterView, CustomAuthToken

# Router for ViewSets
router = DefaultRouter()
router.register(r'activities', ActivityViewSet)
router.register(r'workout-plans', WorkoutPlanViewSet)
router.register(r'diet-logs', DietLogViewSet)

# URL patterns
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('', include(router.urls)),  # Include the router-generated URLs for activities, workout plans, and diet logs
    path('activities/<int:pk>/', ActivityViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='activity-detail'),
    path('workout-plans/<int:pk>/', WorkoutPlanViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='workout-plan-detail'),
    path('diet-logs/<int:pk>/', DietLogViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='diet-log-detail'),
]
