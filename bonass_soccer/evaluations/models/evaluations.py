from django.db import models

from django.utils.translation import gettext_lazy as _

from bonass_soccer.evaluations.models.period import Period
from bonass_soccer.players.models import Player
from bonass_soccer.utils.models import AbstractBaseModel


# Create your models here.
class PeriodicEvaluationSheet(AbstractBaseModel):
    pace = models.IntegerField(_("Vitesse et Acceleration"))
    assist = models.IntegerField(_("Passe"))
    defense = models.IntegerField(_("defense"))
    shoot = models.IntegerField(_("Puissance du tir"))
    dribble = models.IntegerField(_("Dribble"))
    # physic = models.IntegerField(_("condition physique"), blank=True, null=True)
    # overall = models.IntegerField(_("Evaluation globale"), blank=True, null=True)

    class Meta:
        verbose_name = _("Fiche evaluation periodique")
        verbose_name_plural = _("Fiches evaluation periodique")

    def __str__(self):
        return f"Fiche evaluation {self.pk}"


class Evaluation(AbstractBaseModel):
    examiner = models.OneToOneField(
        Player,
        on_delete=models.CASCADE,
        related_name="evaluations_made",
    )
    player_examined = models.OneToOneField(
        Player,
        on_delete=models.CASCADE,
        related_name="evaluations_received",
    )
    evaluation_period = models.ForeignKey(
        Period,
        on_delete=models.CASCADE,
        related_name="period_evaluations"
    )
    evaluation_sheet = models.ForeignKey(
        PeriodicEvaluationSheet,
        on_delete=models.CASCADE,
        related_name="evaluations",
    )

    def clean(self):
        if self.examiner_id == self.player_examined_id:
            raise Exception("Tu ne peux pas t'auto evaluer")
        super().clean()

