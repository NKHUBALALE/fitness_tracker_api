from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user who logged the activity
    activity_type = models.CharField(max_length=50)  # e.g., Running, Cycling
    duration = models.PositiveIntegerField()  # Duration in minutes
    distance = models.FloatField()  # Distance in km or miles
    calories_burned = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)  # Automatically set to now when created

    def __str__(self):
        return f"{self.activity_type} by {self.user.username} on {self.date}"

class WorkoutPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class DietLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.CharField(max_length=100)
    calories = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.food_item} logged by {self.user.username} on {self.date}"