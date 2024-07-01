from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Club(models.Model):
    mongo_id = models.CharField(max_length=24, unique=True)  # Storing the MongoDB _id as a string
    name = models.CharField(max_length=255)
    founded = models.IntegerField()
    stadium = models.CharField(max_length=255)
    location = models.JSONField()  # Using JSONField to store the location object
    players = models.JSONField()  # Using JSONField to store the array of players

    def __str__(self):
        return self.name


class Match(models.Model):
    STATUS_CHOICES = [
        ('Upcoming', 'Upcoming'),
        ('Completed', 'Completed'),
    ]

    home_team = models.ForeignKey(Club, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Club, related_name='away_matches', on_delete=models.CASCADE)
    competition = models.CharField(max_length=255)
    venue = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    attendance = models.IntegerField()
    referee = models.CharField(max_length=255)
    season = models.CharField(max_length=50)
    win_team = models.ForeignKey(Club, related_name='won_matches', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} - {self.competition}"
