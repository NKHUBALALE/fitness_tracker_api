# serializers.py
from rest_framework import serializers
from .models import Activity, WorkoutPlan, DietLog

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'  # Specify fields as needed, e.g., ['id', 'user', 'activity_type', ...]

class WorkoutPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutPlan
        fields = '__all__'

class DietLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietLog
        fields = ['id', 'user', 'food_item', 'calories', 'date']  # Specify only relevant fields
        read_only_fields = ['user', 'date']  # User and date should be set automatically
