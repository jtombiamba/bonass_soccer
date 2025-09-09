import datetime
import json
from http import HTTPStatus

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse

from bonass_soccer.players.models import GameRating, Player, Organisation, Team, Game
from bonass_soccer.utils.compute_random_distribution import RandomDistribution


def slider_view(request):
    return render(request, "slider.html")

def randomize_players(request):
    # Simulate fetching data dynamically
    if request.method == 'GET':
        data = {
            'message': 'This is dynamic data!',
            'content': 'This content was loaded without refreshing the page.',
        }
        return JsonResponse(data)
    elif request.method == 'POST':
        # data = request.POST
        data = json.loads(request.body)
        secret_code = data.get("secret_code", "")
        # TODO: Temporary
        # Check if teams of the day already exist
        teams = Team.objects.filter(game__date=datetime.date.today())
        if teams.exists():
            content_data = {}
            for team in teams:
                if team.name not in content_data:
                    content_data[team.name] = [member.name for member in team.members.all()]
            data = {
                'message': 'Teams already made!!! Here they are: ',
                'content': content_data,
            }
            return JsonResponse(data)

        game, created = Game.objects.get_or_create(date=datetime.date.today())
        if secret_code != game.code:
            content_data = {
                "Team #1": [],
                "Team #2": [],
            }
            data = {
                'message': 'Tu ne peux pas generer les equipes sans le bon code: ',
                'content': content_data,
            }
            return JsonResponse(data)
        players_rating_id = list(GameRating.objects.filter(
            game__date=datetime.date.today()
        ).values("player_id", "physic").all())
        print(f"players rating id = {players_rating_id}")
        random_distribution = RandomDistribution([x["player_id"] for x in players_rating_id], [x["physic"] for x in players_rating_id])
        first_sample, second_sample = random_distribution.generate()
        if len(first_sample) == 0:
            content_data = {
                "Team #1": [],
                "Team #2": [],
            }
            data = {
                'message': 'No players for the moment: ',
                'content': content_data,
            }
            return JsonResponse(data)
        team1 = Team.objects.create(name="Team #1", game_id=game.pk)
        team2 = Team.objects.create(name="Team #2", game_id=game.pk)
        team1.members.set(list(Player.objects.filter(pk__in=first_sample).all()))
        team2.members.set(list(Player.objects.filter(pk__in=second_sample).all()))
        content_data = {}
        for team in teams:
            if team.name not in content_data:
                content_data[team.name] = [member.name for member in team.members.all()]
        print(f"content data = {content_data}")
        # content_data = {
        #     "Team #1": ["Glen", "Core", "Tim", "Paul", "John"],
        #     "Team #2": ["Andrew", "Simon", "Chad", "Tom", "James"],
        # }
        data = {
            'message': 'This is a successful pseudo random Generation of Teams! here they are: ',
            'content': content_data,
        }
        return JsonResponse(data)

def index_view(request):
    players_rating_id = GameRating.objects.filter(game__date=datetime.date.today()).values_list("player_id", flat=True)
    players = Player.objects.filter(pk__in=players_rating_id)
    return render(
        request,
        "random_call.html",
        {
            "date": datetime.date.today(),
            "players": players
        }
    )

def create_performance_note(request):
    if request.method == "POST":
        # you can save your data into json format
        # data = json.dumps(request.POST.get("data", None))
        data = request.POST.get("data", None)
        try:
            organisation = Organisation.objects.get(pk=int(data["organisation_id"]))
        except Organisation.DoesNotExist:
            return JsonResponse({"message": "Unknown Organisation"})

        return JsonResponse({"message": "Success"})



# # views.py
# from rest_framework import generics, permissions, status
# from rest_framework.response import Response
# from .models import PerformanceNote, Team
# from .serializers import PerformanceNoteSerializer
# from django.contrib.auth import get_user_model
#
# User = get_user_model()
#
#
# class CreatePerformanceNoteView(generics.CreateAPIView):
#     serializer_class = PerformanceNoteSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def perform_create(self, serializer):
#         team_id = self.kwargs['team_id']
#         team = generics.get_object_or_404(Team, id=team_id)
#
#         # Ensure the sender is a team member
#         if not team.members.filter(id=self.request.user.id).exists():
#             return Response(
#                 {"detail": "You are not a member of this team"},
#                 status=status.HTTP_403_FORBIDDEN
#             )
#
#         serializer.save(
#             sender=self.request.user,
#             team=team
#         )
#
#
# class PerformanceNoteSerializer(serializers.ModelSerializer):
#     receiver = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all(),
#         required=True
#     )
#
#     class Meta:
#         model = PerformanceNote
#         fields = ['receiver', 'note']
#         read_only_fields = ['sender', 'team']
#
#     def validate_receiver(self, value):
#         request = self.context.get('request')
#         team_id = self.context.get('view').kwargs['team_id']
#
#         # Check receiver is in the same team
#         if not Team.objects.filter(id=team_id, members=value).exists():
#             raise serializers.ValidationError(
#                 "Receiver must be a member of the same team"
#             )
#
#         # Prevent self-review
#         if value == request.user:
#             raise serializers.ValidationError(
#                 "You cannot create a performance note for yourself"
#             )
#
#         return value