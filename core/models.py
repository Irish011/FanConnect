from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from bson.objectid import ObjectId
from db_connections import matches_collection, predictions_collections, user_collection
# from core.task import update_predictions_and_rewards


class Club(models.Model):
    mongo_id = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=255)
    founded = models.IntegerField()
    stadium = models.CharField(max_length=255)
    location = models.JSONField()
    players = models.JSONField()

    def __str__(self):
        return self.name


class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match_id = models.CharField(max_length=24)
    win_team_id = models.CharField(max_length=24)

    def __str__(self):
        return f"Prediction by {self.user} for match {self.match_id} predicting team {self.win_team_id}"


class Match(models.Model):
    STATUS_CHOICES = [
        ('Upcoming', 'Upcoming'),
        ('Completed', 'Completed'),
    ]

    mongo_id = models.CharField(max_length=24, unique=True)
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
    win_team = models.ForeignKey(Club, related_name='win_matches', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} - {self.competition}"


@receiver(post_save, sender=Match)
def update_match_status(sender, instance, **kwargs):
    if instance.status == 'Completed' and instance.win_team:
        match_id = instance.mongo_id
        print(match_id)
        if instance.win_team is None:
            win_team_id = ""
        else:
            win_team_id = instance.win_team.mongo_id
        print(win_team_id)
        # update_predictions_and_rewards.delay(match_id, win_team_id)
        # def update_predictions_and_rewards(match_id, win_team_id):

        matches_collection.update_one(
            {'_id': ObjectId(match_id)},
            {'$set': {'status': 'Completed', 'win_team_id': ObjectId(win_team_id)}}
        )

        predictions = list(
            predictions_collections.find({'match_id': ObjectId(match_id), 'win_team_id': ObjectId(win_team_id)}))
        if predictions:
            print("Present", predictions)

        for prediction in predictions:
            user_id = prediction['user_id']
            user_collection.update_one(
                {'_id': ObjectId(user_id)},
                {'$inc': {'rewards': 1}}
            )
