from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.ImageField(upload_to='logos/')

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title


# class Match(models.Model):
#     STATUS_CHOICES = [
#         ('Upcoming', 'Upcoming'),
#         ('Completed', 'Completed'),
#     ]
#
#     home_team = models.CharField(max_length=100)
#     away_team = models.CharField(max_length=100)
#     date = models.DateTimeField()
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES,
#                               default='Upcoming')
#
#     def __str__(self):
#         return f"{self.home_team} vs {self.away_team} on {self.date}"
