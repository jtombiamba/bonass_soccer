# models.py
from django.db import models


class BaseForm(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)


class Page(models.Model):
    form = models.ForeignKey(BaseForm, on_delete=models.CASCADE, related_name='pages')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class Question(models.Model):
    ANSWER_TYPES = [
        ('BOOLEAN', 'Yes/No'),
        ('STRING', 'Text'),
        ('NUMBER', 'Number'),
        ('DATE', 'Date'),
        ('RANGE', 'Range'),
        ('MULTIPLE_CHOICE', 'Multiple Choice'),
    ]

    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=500)
    answer_type = models.CharField(max_length=20, choices=ANSWER_TYPES)
    required = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    # For range questions
    range_min = models.IntegerField(default=0)
    range_max = models.IntegerField(default=100)

    class Meta:
        ordering = ['order']


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)