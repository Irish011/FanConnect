from django.contrib import admin
from .models import Match, Club

# Register your models here.



class MatchAdmin(admin.ModelAdmin):
    list_display = ('home_team', 'away_team', 'competition', 'date', 'status')
    list_filter = ('status', 'competition')
    search_fields = ('home_team__name', 'away_team__name', 'competition')


admin.site.register(Club)
admin.site.register(Match, MatchAdmin)
