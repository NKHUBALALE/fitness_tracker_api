# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User  # Import the User model
from .models import Activity, WorkoutPlan, DietLog

# Activity Serializer
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'  # Specify fields as needed, e.g., ['id', 'user', 'activity_type', ...]

# WorkoutPlan Serializer
class WorkoutPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutPlan
        fields = '__all__'

# DietLog Serializer
class DietLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietLog
        fields = ['id', 'user', 'food_item', 'calories', 'date']  # Specify only relevant fields
        read_only_fields = ['user', 'date']  # User and date should be set automatically

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # Add any other fields you need
