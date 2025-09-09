from django.db import models

from bonass_soccer.form_manager.models.models import BaseForm, Question, Choice


class FormResponse(models.Model):
    form = models.ForeignKey(BaseForm, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey("players.Player", on_delete=models.CASCADE)


class Answer(models.Model):
    response = models.ForeignKey(FormResponse, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    # Different answer types
    boolean_value = models.BooleanField(null=True, blank=True)
    string_value = models.CharField(max_length=500, null=True, blank=True)
    number_value = models.FloatField(null=True, blank=True)
    date_value = models.DateField(null=True, blank=True)
    range_value = models.IntegerField(null=True, blank=True)
    choices = models.ManyToManyField(Choice, blank=True)