from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Activity, WorkoutPlan, DietLog
from .serializers import ActivitySerializer, WorkoutPlanSerializer, DietLogSerializer
from rest_framework.authtoken.views import ObtainAuthToken

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

# Register API view
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]  # Allow any user to register

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        token = Token.objects.create(user=user)
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = response.data['token']
        return Response({'token': token})