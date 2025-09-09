from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from bonass_soccer.evaluations.models.evaluations import PeriodicEvaluationSheet, Evaluation
from bonass_soccer.evaluations.models.period import Period

class PeriodAdmin(ModelAdmin):
    list_display = ["id", "number_eval_per_player"]
    fields = ["number_eval_per_player"]

# Register your models here.
class PeriodicEvaluationSheetAdmin(ModelAdmin):
    list_display = ["id"]
    fields = ["pace", "assist", "defense", "shoot", "dribble"]


class EvaluationAdmin(ModelAdmin):
    list_display = ["id", "player_examined", "examiner", "evaluation_period", "evaluation_sheet"]
    fields = ["player_examined", "examiner", "evaluation_period", "evaluation_sheet"]

admin.site.register(Period, PeriodAdmin)
admin.site.register(Evaluation, EvaluationAdmin)
admin.site.register(PeriodicEvaluationSheet, PeriodicEvaluationSheetAdmin)