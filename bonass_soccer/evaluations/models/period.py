from bonass_soccer.utils.models import AbstractBaseModel
from django.db.models import IntegerField

class Period(AbstractBaseModel):
    # the number of players a given player can evaluate during the period
    number_eval_per_player = IntegerField()


    def __str__(self):
        return f"Periode {self.pk}"