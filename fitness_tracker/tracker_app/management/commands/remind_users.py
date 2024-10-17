from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from tracker_app.models import Activity  # Adjust this import based on your app structure

class Command(BaseCommand):
    help = 'Remind users to exercise if they haven\'t been active for 24 hours'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        threshold_time = now - timedelta(hours=24)

        # Find users who have not logged any activity in the last 24 hours
        inactive_users = User.objects.filter(activity__date__lt=threshold_time).distinct()

        for user in inactive_users:
            self.send_reminder(user)

    def send_reminder(self, user):
        # Implement your notification logic here (e.g., print to console)
        print(f"Reminder: {user.username}, it's time to exercise!")