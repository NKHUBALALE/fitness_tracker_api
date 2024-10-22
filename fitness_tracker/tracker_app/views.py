from rest_framework.permissions import IsAuthenticated
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
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter

# Home view
def home(request):
    """
    A simple home view to test the API.
    """
    return HttpResponse("Welcome to the Fitness Tracker API!")

# Custom pagination class for user activity history
class UserActivityHistoryPagination(PageNumberPagination):
    """
    Custom pagination class for user activity history.
    """
    page_size = 10  # Default number of activities per page
    page_size_query_param = 'page_size'  # Allow clients to set the page size
    max_page_size = 100  # Limit to prevent excessively large pages

# Activity ViewSet with permission checks
class ActivityViewSet(viewsets.ModelViewSet):
    """
    A viewset that allows users to create, retrieve, update, and delete activities.
    The user must be authenticated to access their activities.
    """
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Returns a queryset filtered by the logged-in user.
        """
        return Activity.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically assigns the logged-in user to the activity when created.
        """
        serializer.save(user=self.request.user)

# User Activity History View
class UserActivityHistoryView(generics.ListAPIView):
    """
    A view to retrieve the activity history of a logged-in user.
    Supports optional filtering by activity type or a date range.
    """
    serializer_class = ActivitySerializer # Use custom serializer to serialize activity data
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = UserActivityHistoryPagination  # Use custom pagination
    filter_backends = (OrderingFilter,)  # Enable ordering
    ordering_fields = ['date', 'duration', 'calories_burned']  # Fields that can be ordered
    ordering = ['date']  # Default ordering

    def get_queryset(self):
        """
        Filters the activities of the user with optional filtering by activity type and date range.
        """
        user = self.request.user # Get the logged-in user
        queryset = Activity.objects.filter(user=user) ## activities of the user

        # Optional filtering by activity type
        activity_type = self.request.query_params.get('activity_type')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        # Apply filters if provided
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        return queryset

# WorkoutPlan ViewSet
class WorkoutPlanViewSet(viewsets.ModelViewSet):
    """
    A viewset to manage workout plans.
    Only authenticated users can create or view workout plans.
    """
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer
    permission_classes = [permissions.IsAuthenticated]  # Restrict access to authenticated users

# DietLog ViewSet
class DietLogViewSet(viewsets.ModelViewSet):
    """
    A viewset to manage diet logs.
    Only authenticated users can create or view their diet logs.
    """
    queryset = DietLog.objects.all()
    serializer_class = DietLogSerializer
    permission_classes = [permissions.IsAuthenticated]  # Restrict access to authenticated users

# DietLog ListCreateView
class DietLogListCreateView(generics.ListCreateAPIView):
    """
    A view that allows listing and creating diet logs for authenticated users.
    Automatically assigns the logged-in user to the created log.
    """
    queryset = DietLog.objects.all()
    serializer_class = DietLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Automatically assigns the logged-in user to the created diet log.
        """
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        Returns the queryset filtered by the logged-in user.
        """
        return self.queryset.filter(user=self.request.user)

# User list view
class UserListView(generics.ListAPIView):
    """
    A view to retrieve a list of all registered users.
    Only accessible by authenticated users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# Register API view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import permissions

class RegisterView(APIView):
    """
    A view that handles user registration.
    Allows any user to register and get JWT tokens upon successful registration.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Handles POST requests for user registration.
        """
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        user = User.objects.create_user(username=username, password=password, email=email)

        # Generate JWT tokens (access and refresh)
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        # Return the tokens in the response
        return Response({
            'refresh': str(refresh),
            'access': str(access)
        }, status=status.HTTP_201_CREATED)

# Custom Auth Token view
class CustomAuthToken(ObtainAuthToken):
    """
    A custom view to obtain an authentication token.
    Overrides the default behavior to return only the token.
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = response.data['token']
        return Response({'token': token})

# Progress view (expanded metrics)
class ProgressView(APIView):
    """
    A view that provides progress metrics for the logged-in user.
    Displays total distance, calories burned, and duration, as well as weekly and monthly metrics.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Handles GET requests to return progress metrics for the user.
        """
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

        # Prepare the response data
        progress_data = {
            'total_distance': total_distance,
            'total_calories': total_calories,
            'total_duration': total_duration,
            'weekly_progress': weekly_data,
            'monthly_progress': monthly_data,
        }

        return Response(progress_data)

    def calculate_weekly_metrics(self, user):
        """
        Calculates the total distance, calories burned, and duration for the last 7 days.
        """
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
        """
        Calculates the total distance, calories burned, and duration for the last 30 days.
        """
        last_month = timezone.now() - timedelta(days=30)
        monthly_distance = Activity.objects.filter(user=user, date__gte=last_month).aggregate(Sum('distance'))['distance__sum'] or 0
        monthly_calories = Activity.objects.filter(user=user, date__gte=last_month).aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0
        monthly_duration = Activity.objects.filter(user=user, date__gte=last_month).aggregate(Sum('duration'))['duration__sum'] or 0

        return {
            'distance': monthly_distance,
            'calories': monthly_calories,
            'duration': monthly_duration,
        }
