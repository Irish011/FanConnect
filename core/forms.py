from django import forms
from db_connections import club_collection
from bson.objectid import ObjectId
from bson.errors import InvalidId


class UserForm(forms.Form):
    username = forms.CharField(max_length=100)
    age = forms.IntegerField()
    email = forms.EmailField()
    mobile_number = forms.CharField(max_length=15)
    country = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())
    favorite_clubs = forms.MultipleChoiceField(choices=[], widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        clubs = list(club_collection.find())
        club_choices = [(str(club['_id']), club['name']) for club in clubs]
        self.fields['favorite_clubs'].choices = club_choices

    def clean_favorite_club(self):
        favorite_clubs = self.cleaned_data['favorite_clubs']

        if len(favorite_clubs) > 3:
            raise forms.ValidationError("You can select upto 3 favorite clubs only.")
        try:
            favorite_clubs = [ObjectId(club_id) for club_id in favorite_clubs]
        except InvalidId:
            raise forms.ValidationError("Invalid club ID format")
        return favorite_clubs


class UsersForm(forms.Form):
    favorite_clubs = forms.MultipleChoiceField(choices=[], widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super(UsersForm, self).__init__(*args, **kwargs)
        # Dynamically set choices for favorite_clubs from the club collection
        clubs = list(club_collection.find())
        club_choices = [(str(club['_id']), club['name']) for club in clubs]
        self.fields['favorite_clubs'].choices = club_choices

    def clean_favorite_club(self):
        favorite_clubs = self.cleaned_data['favorite_clubs']

        try:
            favorite_clubs = [ObjectId(club_id) for club_id in favorite_clubs]
        except InvalidId:
            raise forms.ValidationError("Invalid club ID format")

        return favorite_clubs
