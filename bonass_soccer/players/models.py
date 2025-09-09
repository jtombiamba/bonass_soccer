from django.db import models
from django.utils.translation import gettext_lazy as _

from bonass_soccer.evaluations.models.period import Period

from django.core.exceptions import ValidationError

from bonass_soccer.utils.models import AbstractBaseModel


class Organisation(AbstractBaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Organisation {self.name}"

# Create your models here.
class Player(models.Model):
    name = models.CharField(_("Nom"), max_length=25)
    # V1: tout en dur
    # TODO: upgrade
    phone = models.CharField(_("Numéro de telephone whatsapp"), max_length=10)
    secret = models.CharField(_("code secret"), max_length=10)
    organisation = models.ForeignKey(
        Organisation,
        related_name="players",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name}"


class Game(models.Model):
    date = models.DateField()
    code = models.CharField(null=True, blank=True, max_length=25)
    players = models.ManyToManyField(
        "Player",
        through="GameRating",
    )

    def __str__(self):
        return f"Match du {self.date}"

class Team(models.Model):
    name = models.CharField(max_length=100)
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
    )
    members = models.ManyToManyField(Player, related_name='teams')

    def __str__(self):
        return f"Team {self.name}"


class GameRating(AbstractBaseModel):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
    )
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
    )
    period = models.ForeignKey(
        Period,
        on_delete=models.CASCADE,
    )
    physic = models.IntegerField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['game', 'player'], name='unique_game_player')
        ]

    def __str__(self):
        return f"Joueur {self.player_id} du match {self.game_id}"

    def build_ratings(self):
        # retrieve fo every player the average categories ratings and compute the overall with the physic value entered
        # you will retrieve a list of players with overall ratings to pass to the random distributor
        # def compute_overall_rating(self):
        #     self.overall = int(
        #         0.3 * self.physic +
        #         0.15 * self.pace +
        #         0.15 * self.assist +
        #         0.15 * self.shoot +
        #         0.15 * self.defense +
        #         0.1 * self.dribble
        #     )
        #     self.save()
        pass

class PerformanceNote(AbstractBaseModel):
    sender = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='sent_notes'
    )
    receiver = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='received_notes'
    )
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    note = models.FloatField() # models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['sender', 'receiver', 'organisation'],
                name='unique_feedback_per_team'
            )
        ]

    def clean(self):
        # Prevent self-reviews
        if self.sender == self.receiver:
            raise ValidationError("Players cannot review themselves")

        # Ensure both players belong to the same team
        if not self.organisation.players.filter(id=self.sender.id).exists():
            raise ValidationError("Sender must be an organisation member")

        if not self.organisation.players.filter(id=self.receiver.id).exists():
            raise ValidationError("Receiver must be an organisation member")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sender} -> {self.receiver} in {self.organisation}"