import operator
from typing import Callable

from django.db import models

from bonass_soccer.form_manager.models.models import Question

def between(a: int| float, b: int | float, c: int | float) -> bool:
    return a <=b <= c

class Condition(models.Model):
    LOGIC_TYPES = [('AND', 'All of'), ('OR', 'Any of')]

    target_question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='display_conditions'
    )
    logic_type = models.CharField(max_length=3, choices=LOGIC_TYPES)

class Operator(models.enums.TextChoices):
    NE = "NE", "Not Equal",
    EQ = "EQ", "Equal",
    LE = "LE", "Lower or Equal"
    LT = "LT", "Lower Than",
    GE = "GE", "Greater or Equal",
    GT = "GT", "Greater Than"
    BT = "BT", "Between",
    ANY = "any", "Any",
    __empty__ = "No operator selected"

    @property
    def value_to_operator(self) -> dict[str, Callable]:
        return {
            "NE": operator.__ne__,
            "EQ": operator.__eq__,
            "LE": operator.__le__,
            "LT": operator.__lt__,
            "GE": operator.__ge__,
            "GT": operator.__gt__,
            "BT": between,
        }

    def operator_func(self) -> Callable:
        return self.value_to_operator[self.value]


class ConditionClause(models.Model):
    OPERATORS = [
        ('EQUALS', '='),
        ('NOT_EQUALS', '≠'),
        ('GT', '>'),
        ('LT', '<'),
        ('GTE', '≥'),
        ('LTE', '≤'),
    ]

    condition = models.ForeignKey(Condition, on_delete=models.CASCADE, related_name='clauses')
    source_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    operator = models.CharField(max_length=10, choices=Operator.choices)
    expected_value = models.CharField(max_length=200)  # Store as string for flexibility