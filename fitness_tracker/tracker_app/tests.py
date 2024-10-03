from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Activity  # Ensure you import your Activity model

class ActivityAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
        self.token = Token.objects.create(user=self.user)

        # Create an activity for testing
        self.activity = Activity.objects.create(
            user=self.user,
            activity_type='Running',
            duration=30,
            distance=5.0,
            calories_burned=300
        )

    def test_activity_list_authenticated(self):
        # Use the token for authentication
        response = self.client.get(reverse('activity-list'), HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, 200)
        
        # Check if the response contains the expected activity type
        self.assertContains(response, "Running")  # Replace with actual expected content

    def test_create_activity_authenticated(self):
        response = self.client.post(reverse('activity-list'), {
            'user': self.user.id,
            'activity_type': 'Jogging',
            'duration': 45,
            'distance': 7.5,
            'calories_burned': 400
        }, HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.assertEqual(response.status_code, 201)  # Check for successful creation