from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Activity, WorkoutPlan, DietLog  # Ensure you import your models

class ActivityAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
        self.token = Token.objects.create(user=self.user)

        self.activity = Activity.objects.create(
            user=self.user,
            activity_type='Running',
            duration=30,
            distance=5.0,
            calories_burned=300
        )

    def test_activity_list_authenticated(self):
        response = self.client.get(reverse('activity-list'), HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Running")

    def test_create_activity_authenticated(self):
        response = self.client.post(reverse('activity-list'), {
            'user': self.user.id,
            'activity_type': 'Jogging',
            'duration': 45,
            'distance': 7.5,
            'calories_burned': 400
        }, HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.assertEqual(response.status_code, 201)  # Check for successful creation

    def test_create_activity_missing_fields(self):
        response = self.client.post(reverse('activity-list'), {
            'user': self.user.id,
            'activity_type': '',  # Missing activity_type
            'duration': 45,
            'distance': 7.5,
            'calories_burned': 400
        }, HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.assertEqual(response.status_code, 400)  # Bad request
        self.assertIn("This field may not be blank.", response.data['activity_type'])

    def test_create_activity_invalid_duration(self):
        response = self.client.post(reverse('activity-list'), {
            'user': self.user.id,
            'activity_type': 'Running',
            'duration': -10,  # Invalid duration
            'distance': 5.0,
            'calories_burned': 300
        }, HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.assertEqual(response.status_code, 400)  # Bad request
        self.assertIn("Ensure this value is greater than or equal to 0.", response.data['duration'])

    def test_activity_list_unauthenticated(self):
        response = self.client.get(reverse('activity-list'))
        self.assertEqual(response.status_code, 401)  # Unauthorized

    def test_update_activity_authenticated(self):
        response = self.client.put(
            reverse('activity-detail', args=[self.activity.id]), 
            {
                'user': self.user.id,
                'activity_type': 'Walking',
                'duration': 50,
                'distance': 8.0,
                'calories_burned': 500
            }, 
            HTTP_AUTHORIZATION='Token ' + self.token.key,
            content_type='application/json'  # Set the content type to JSON
        )
    
        self.assertEqual(response.status_code, 200)  # Check for successful update
        self.activity.refresh_from_db()  # Refresh the instance from the database
        self.assertEqual(self.activity.activity_type, 'Walking')

    def test_delete_activity_authenticated(self):
        response = self.client.delete(reverse('activity-detail', args=[self.activity.id]), HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, 204)  # No Content
        self.assertFalse(Activity.objects.filter(id=self.activity.id).exists())  # Check that the activity is deleted

    def test_create_activity_invalid_calories_burned(self):
        response = self.client.post(reverse('activity-list'), {
            'user': self.user.id,
            'activity_type': 'Swimming',
            'duration': 30,
            'distance': 2.5,
            'calories_burned': -200  # Invalid calories burned
        }, HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.assertEqual(response.status_code, 400)  # Bad request
        self.assertIn("Ensure this value is greater than or equal to 0.", response.data['calories_burned'])


class WorkoutPlanAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
        self.token = Token.objects.create(user=self.user)

        self.workout_plan = WorkoutPlan.objects.create(
            user=self.user,
            name='Beginner Workout',
            description='A simple workout plan for beginners.'
        )

    def test_workout_plan_list_authenticated(self):
        response = self.client.get(reverse('workout-plan-list'), HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Beginner Workout")

    def test_create_workout_plan_authenticated(self):
        response = self.client.post(reverse('workout-plan-list'), {
            'user': self.user.id,
            'name': 'Advanced Workout',
            'description': 'A challenging workout plan for advanced users.'
        }, HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.assertEqual(response.status_code, 201)  # Check for successful creation

    def test_create_workout_plan_missing_fields(self):
        response = self.client.post(reverse('workout-plan-list'), {
            'user': self.user.id,
            'name': '',  # Missing name
            'description': 'This should fail due to missing name.'
        }, HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.assertEqual(response.status_code, 400)  # Bad request
        self.assertIn("This field may not be blank.", response.data['name'])

    def test_update_workout_plan_authenticated(self):
        response = self.client.put(
            reverse('workout-plan-detail', args=[self.workout_plan.id]),  # Update URL
            {
                'user': self.user.id,
                'name': 'Intermediate Workout',
                'description': 'An intermediate workout plan for users.'
            },
            HTTP_AUTHORIZATION='Token ' + self.token.key,
            content_type='application/json'  # Set the content type to JSON
        )

        self.assertEqual(response.status_code, 200)  # Check for successful update
        self.workout_plan.refresh_from_db()  # Refresh the instance from the database
        self.assertEqual(self.workout_plan.name, 'Intermediate Workout')

    def test_delete_workout_plan_authenticated(self):
        response = self.client.delete(reverse('workout-plan-detail', args=[self.workout_plan.id]), HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, 204)  # No Content
        self.assertFalse(WorkoutPlan.objects.filter(id=self.workout_plan.id).exists())  # Check that the workout plan is deleted

    

class DietLogAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
        self.token = Token.objects.create(user=self.user)

        self.diet_log = DietLog.objects.create(
            user=self.user,
            food_item='Apple',
            calories=95
        )

    def test_diet_log_list_authenticated(self):
        response = self.client.get(reverse('diet-log-list-create'), HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Apple")

    def test_create_diet_log_authenticated(self):
        response = self.client.post(reverse('diet-log-list-create'), {
            'user': self.user.id,
            'food_item': 'Banana',
            'calories': 105
        }, HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, 201)  # Check for successful creation

    def test_create_diet_log_missing_fields(self):
        response = self.client.post(reverse('diet-log-list-create'), {
            'user': self.user.id,
            'food_item': '',  # Missing food_item
            'calories': 105
        }, HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.assertEqual(response.status_code, 400)  # Bad request
        self.assertIn("This field may not be blank.", response.data['food_item'])

    def test_update_diet_log_authenticated(self):
        response = self.client.put(
            reverse('diet-log-detail', args=[self.diet_log.id]),
            {
                'user': self.user.id,
                'food_item': 'Orange',
                'calories': 62
            },
            HTTP_AUTHORIZATION='Token ' + self.token.key,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.diet_log.refresh_from_db()
        self.assertEqual(self.diet_log.food_item, 'Orange')

    def test_delete_diet_log_authenticated(self):
        response = self.client.delete(reverse('diet-log-detail', args=[self.diet_log.id]), HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(DietLog.objects.filter(id=self.diet_log.id).exists())
