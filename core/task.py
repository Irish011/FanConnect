from bson.objectid import ObjectId
from celery import shared_task
from db_connections import predictions_collections, user_collection, matches_collection


@shared_task
def update_predictions_and_rewards(match_id, win_team_id):

    matches_collection.update_one(
        {'_id': ObjectId(match_id)},
        {'$set': {'status': 'Completed', 'win_team_id': ObjectId(win_team_id)}}
    )

    predictions = list(predictions_collections.find({'match_id': ObjectId(match_id), 'win_team_id': ObjectId(win_team_id)}))
    if predictions:
        print("Present", predictions)

    for prediction in predictions:
        user_id = prediction['user_id']
        user_collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$inc': {'rewards': 1}}
        )
