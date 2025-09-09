import json

from django.shortcuts import render, get_object_or_404

from bonass_soccer.form_manager.models.models import BaseForm, Question


# Create your views here.
# views.py
def form_view(request, form_id):
    form = get_object_or_404(BaseForm, pk=form_id)

    # Preload conditions data
    questions_with_conditions = []
    for question in Question.objects.filter(display_conditions__isnull=False):
        conditions = []
        for condition in question.display_conditions.all():
            clauses = [{
                'source_question_id': c.source_question_id,
                'operator': c.operator,
                'expected_value': c.expected_value
            } for c in condition.clauses.all()]
            conditions.append({'logic_type': condition.logic_type, 'clauses': clauses})

        questions_with_conditions.append({
            'id': question.id,
            'conditions': conditions
        })

    return render(request, 'form.html', {
        'form': form,
        'conditions_data': json.dumps(questions_with_conditions)
    })