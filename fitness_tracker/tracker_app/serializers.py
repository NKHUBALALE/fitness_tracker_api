# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User  # Import the User model
from .models import Activity, WorkoutPlan, DietLog

# Activity Serializer
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'user', 'activity_type', 'duration', 'distance', 'calories_burned', 'date']
        read_only_fields = ['user', 'date']  # User and date should be set automatically

    def validate_activity_type(self, value):
        
        if not value:
            raise serializers.ValidationError("Activity type is required.")
        return value

    def validate_duration(self, value):
        if value <= 0:
            raise serializers.ValidationError("Duration must be greater than zero.")
        return value

    def validate_distance(self, value):
        if value < 0:
            raise serializers.ValidationError("Distance cannot be negative.")
        return value

    def validate_calories_burned(self, value):
        if value < 0:
            raise serializers.ValidationError("Calories burned cannot be negative.")
        return value

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
