from django.contrib import admin
from django.contrib.admin import ModelAdmin

from bonass_soccer.players.models import Game, Player, GameRating, Organisation, Team


class OrganisationAdmin(ModelAdmin):
    list_display = ["id", "name"]
    fields = ["name"]

# Register your models here.
class PlayerAdmin(ModelAdmin):
    list_display = ["id", "name", "phone", "organisation", "secret"]
    fields = ["name", "phone", "organisation", "secret"]
    # readonly_fields = list_display


class GameAdmin(ModelAdmin):
    list_display = ["id", "date", "code"]
    fields = ["date", "code"]
    # readonly_fields = list_display

class TeamAdmin(ModelAdmin):
    list_display = ["id", "name", "game", "display_players"]

    def display_players(self, obj):
        """
        Custom method to display players as a comma-separated list.
        """
        return ", ".join([player.name for player in obj.members.all()])

    display_players.short_description = 'Players'  # Column header in admin

class GameRatingAdmin(ModelAdmin):
    list_display = ["game", "player", "physic", "period"]
    fields = ["game", "player", "period", "physic"]


admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(GameRating, GameRatingAdmin)