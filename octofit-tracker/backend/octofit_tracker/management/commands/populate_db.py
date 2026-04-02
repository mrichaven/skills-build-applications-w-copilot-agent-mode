from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models
from octofit_tracker import models as octo_models

from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Clear all collections
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create Teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create Users
        users = [
            User(email='tony@stark.com', username='ironman', team=marvel),
            User(email='steve@rogers.com', username='captainamerica', team=marvel),
            User(email='clark@kent.com', username='superman', team=dc),
            User(email='bruce@wayne.com', username='batman', team=dc),
        ]
        for user in users:
            user.set_password('password')
            user.save()

        # Create Activities
        Activity.objects.create(user=users[0], type='run', duration=30)
        Activity.objects.create(user=users[1], type='cycle', duration=45)
        Activity.objects.create(user=users[2], type='swim', duration=60)
        Activity.objects.create(user=users[3], type='yoga', duration=20)

        # Create Workouts
        Workout.objects.create(name='Morning Cardio', description='Cardio for all')
        Workout.objects.create(name='Strength Training', description='Strength for all')

        # Create Leaderboard
        Leaderboard.objects.create(user=users[0], score=100)
        Leaderboard.objects.create(user=users[1], score=90)
        Leaderboard.objects.create(user=users[2], score=110)
        Leaderboard.objects.create(user=users[3], score=95)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data'))

# Models for reference (to be placed in octofit_tracker/models.py):
# class Team(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#
# class Activity(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     type = models.CharField(max_length=50)
#     duration = models.IntegerField()
#
# class Workout(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#
# class Leaderboard(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     score = models.IntegerField()
