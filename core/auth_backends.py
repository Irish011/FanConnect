from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from db_connections import user_collection


class MongoDBBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        user = user_collection.find_one({'username': username})
        if user and check_password(password, user['password']):
            # Create a dummy User object to keep Django happy
            user_obj, created = User.objects.get_or_create(username=username)
            return user_obj
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None