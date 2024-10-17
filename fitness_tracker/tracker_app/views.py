# views.py

from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import Activity, WorkoutPlan, DietLog
from .serializers import ActivitySerializer, WorkoutPlanSerializer, DietLogSerializer, UserSerializer

# Home view
def home(request):
    return HttpResponse("Welcome to the Fitness Tracker API!")

# Activity ViewSet with permission checks
class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter activities by the logged-in user
        return Activity.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the logged-in user to the activity entry
        serializer.save(user=self.request.user)

# User Activity History View
class UserActivityHistoryView(generics.ListAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Activity.objects.filter(user=user)

        # Optional filtering by date range or activity type
        activity_type = self.request.query_params.get('activity_type')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        return queryset

# WorkoutPlan ViewSet
class WorkoutPlanViewSet(viewsets.ModelViewSet):
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer
    permission_classes = [permissions.IsAuthenticated]  # Restrict access to authenticated users

# DietLog ViewSet
class DietLogViewSet(viewsets.ModelViewSet):
    queryset = DietLog.objects.all()
    serializer_class = DietLogSerializer
    permission_classes = [permissions.IsAuthenticated]  # Restrict access to authenticated users

# DietLog ListCreateView
class DietLogListCreateView(generics.ListCreateAPIView):
    queryset = DietLog.objects.all()
    serializer_class = DietLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically assign the logged-in user to the diet log entry
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Filter diet logs by the logged-in user
        return self.queryset.filter(user=self.request.user)

# User list view
class UserListView(generics.ListAPIView):
    """
    Handles GET requests to retrieve a list of users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # Restrict access to authenticated users

# Register API view
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]  # Allow any user to register

    def post(self, request):
        """
        Handles POST requests to register a new user.
        """
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        token = Token.objects.create(user=user)
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)

# Custom Auth Token view
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        """
        Custom post method for ObtainAuthToken to return only the token.
        """
        response = super().post(request, *args, **kwargs)
        token = response.data['token']
        return Response({'token': token})

# Progress view (expanded metrics)
class ProgressView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        # Retrieve optional query parameters for date range
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        # Define the filter for the activity queryset
        filter_kwargs = {'user': user}
        
        # If date range is provided, filter activities
        if start_date and end_date:
            filter_kwargs['date__range'] = [start_date, end_date]

        # Calculate total distance, calories burned, and duration for the logged-in user
        total_distance = Activity.objects.filter(**filter_kwargs).aggregate(Sum('distance'))['distance__sum'] or 0
        total_calories = Activity.objects.filter(**filter_kwargs).aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0
        total_duration = Activity.objects.filter(**filter_kwargs).aggregate(Sum('duration'))['duration__sum'] or 0

        # Calculate weekly and monthly metrics
        weekly_data = self.calculate_weekly_metrics(user)
        monthly_data = self.calculate_monthly_metrics(user)

        progress_data = {
            'total_distance': total_distance,
            'total_calories': total_calories,
            'total_duration': total_duration,
            'weekly_progress': weekly_data,
            'monthly_progress': monthly_data,
        }

        return Response(progress_data)

    def calculate_weekly_metrics(self, user):
        last_week = timezone.now() - timedelta(days=7)
        weekly_distance = Activity.objects.filter(user=user, date__gte=last_week).aggregate(Sum('distance'))['distance__sum'] or 0
        weekly_calories = Activity.objects.filter(user=user, date__gte=last_week).aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0
        weekly_duration = Activity.objects.filter(user=user, date__gte=last_week).aggregate(Sum('duration'))['duration__sum'] or 0

        return {
            'distance': weekly_distance,
            'calories': weekly_calories,
            'duration': weekly_duration,
        }

    def calculate_monthly_metrics(self, user):
        last_month = timezone.now() - timedelta(days=30)
        monthly_distance = Activity.objects.filter(user=user, date__gte=last_month).aggregate(Sum('distance'))['distance__sum'] or 0
        monthly_calories = Activity.objects.filter(user=user, date__gte=last_month).aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0
        monthly_duration = Activity.objects.filter(user=user, date__gte=last_month).aggregate(Sum('duration'))['duration__sum'] or 0

        return {
            'distance': monthly_distance,
            'calories': monthly_calories,
            'duration': monthly_duration,
        }
