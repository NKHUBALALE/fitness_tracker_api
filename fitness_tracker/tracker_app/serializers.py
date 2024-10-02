from rest_framework import serializers
from .models import Activity, WorkoutPlan, DietLog

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'  # or specify fields like ['id', 'user', 'activity_type', ...]

class WorkoutPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutPlan
        fields = '__all__'

class DietLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietLog
        fields = '__all__'