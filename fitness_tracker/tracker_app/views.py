from rest_framework import viewsets
from .models import Activity, WorkoutPlan, DietLog
from .serializers import ActivitySerializer, WorkoutPlanSerializer, DietLogSerializer
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Fitness Tracker API!")

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class WorkoutPlanViewSet(viewsets.ModelViewSet):
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer

class DietLogViewSet(viewsets.ModelViewSet):
    queryset = DietLog.objects.all()
    serializer_class = DietLogSerializer