# views.py
from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Activity, WorkoutPlan, DietLog
from .serializers import ActivitySerializer, WorkoutPlanSerializer, DietLogSerializer, UserSerializer

# Home view
def home(request):
    return HttpResponse("Welcome to the Fitness Tracker API!")

# Activity ViewSet
class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]  # Restrict access to authenticated users

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
        serializer.save(user=self.request.user)  # Automatically assign logged-in user

# User list view
class UserListView(generics.ListAPIView):
    """
    Handles GET requests to retrieve a list of users.

    :queryset: All users in the database
    :serializer_class: UserSerializer
    :permission_classes: IsAuthenticated (only authenticated users can access this view)
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

        :param request: Django's request object
        :return: A JSON response with a token for the newly created user
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
