from django.contrib import admin
from .models import Team, Post

# Register your models here.

admin.site.register(Team)
admin.site.register(Post)

# @admin.register(Match)
# class MatchAdmin(admin.ModelAdmin):
#     list_display = ('home_team', 'away_team', 'date', 'status')
#     list_filter = ('status',)
#     search_fields = ('home_team', 'away_team')
#
#     actions = ['make_completed', 'make_upcoming']
#
#     def make_completed(self, request, queryset):
#         queryset.update(status='Completed')
#     make_completed.short_description = "Mark as Completed"
#
#     def make_upcoming(self, request, queryset):
#         queryset.update(status='Upcoming')
#     make_upcoming.short_description = "Mark selected matches as Upcoming"
#

