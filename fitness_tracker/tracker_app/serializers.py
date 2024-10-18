from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Activity, WorkoutPlan, DietLog

# Activity Serializer
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'  # Specify fields as needed, e.g., ['id', 'user', 'activity_type', ...]

    def validate_activity_type(self, value):
        if value is None or value.strip() == '':
            raise serializers.ValidationError("Activity type is required.")
        return value

    def validate_calories_burned(self, value):
        if value is None or value < 0:
            raise serializers.ValidationError("Calories burned cannot be negative.")
        return value

    def validate_distance(self, value):
        if value is None or value < 0:
            raise serializers.ValidationError("Distance cannot be negative.")
        return value

    def validate_duration(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError("Duration must be greater than zero.")
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
        fields = ['id', 'user', 'food_item', 'calories', 'date']
        read_only_fields = ['user', 'date']

    def validate_calories(self, value):
        if value is None or value < 0:
            raise serializers.ValidationError("Calories cannot be negative.")
        return value


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
