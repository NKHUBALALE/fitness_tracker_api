from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user who logged the activity
    activity_type = models.CharField(max_length=50)  # e.g., Running, walking
    duration = models.PositiveIntegerField()  # Duration in minutes
    distance = models.FloatField()  # Distance in km or miles
    calories_burned = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)  # Automatically set to now when created

    def __str__(self):
        return f"{self.activity_type} by {self.user.username} on {self.date}"

class WorkoutPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user who created the plan
    name = models.CharField(max_length=100)  # Name of the workout plan
    description = models.TextField()  # Description of the workout plan
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set to now when created

    def __str__(self):
        return self.name

class DietLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user who logged the diet
    food_item = models.CharField(max_length=100)  # Name of the food item
    calories = models.PositiveIntegerField()  # Calories in the food item
    date = models.DateTimeField(auto_now_add=True)  # Automatically set to now when created

    def __str__(self):
        return f"{self.food_item} logged by {self.user.username} on {self.date}"
