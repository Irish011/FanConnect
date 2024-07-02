from django.contrib import admin
from .models import Match, Club


# Register your models here.


# class MatchAdmin(admin.ModelAdmin):
#     list_display = ('home_team', 'away_team', 'competition', 'date', 'status')
#     list_filter = ('status', 'competition')
#     list_editable = ('status', 'win_team')
#     search_fields = ('home_team__name', 'away_team__name', 'competition')

class MatchAdmin(admin.ModelAdmin):
    list_display = ('mongo_id', 'home_team', 'away_team', 'status', 'win_team')  # Ensure 'win_team' is in list_display
    list_editable = ('status', 'win_team')


class ClubDetail(admin.ModelAdmin):
    list_display = ('mongo_id', 'name', 'stadium')


admin.site.register(Club, ClubDetail)
admin.site.register(Match, MatchAdmin)
