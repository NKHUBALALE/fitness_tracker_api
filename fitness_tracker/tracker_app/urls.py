from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet, WorkoutPlanViewSet, DietLogViewSet

router = DefaultRouter()
router.register(r'activities', ActivityViewSet)
router.register(r'workout-plans', WorkoutPlanViewSet)
router.register(r'diet-logs', DietLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]