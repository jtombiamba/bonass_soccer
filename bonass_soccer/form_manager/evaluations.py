# utils.py
from bonass_soccer.form_manager.models.responses import Answer


def evaluate_condition(response, condition):
    clauses = condition.clauses.all()
    results = []

    for clause in clauses:
        answer = Answer.objects.filter(
            response=response,
            question=clause.source_question
        ).first()

        if not answer:
            return False  # No answer = condition not met

        actual_value = _get_answer_value(answer)
        expected_value = _cast_value(actual_value, clause.expected_value)

        results.append(_compare_values(actual_value, clause.operator, expected_value))

    if condition.logic_type == 'AND':
        return all(results)
    else:  # OR logic
        return any(results)


def _get_answer_value(answer):
    if answer.question.answer_type == 'BOOLEAN':
        return answer.boolean_value
    elif answer.question.answer_type == 'RANGE':
        return answer.range_value
    # Add other answer types similarly...


def _cast_value(actual_value, expected_value):
    if isinstance(actual_value, bool):
        return expected_value.lower() == 'true'
    elif isinstance(actual_value, (int, float)):
        return float(expected_value)
    # Add other type casting as needed...


def _compare_values(a, operator, b):
    if operator == 'EQUALS':
        return a == b
    elif operator == 'NOT_EQUALS':
        return a != b
    elif operator == 'GT':
        return a > b
    elif operator == 'LT':
        return a < b
    elif operator == 'GTE':
        return a >= b
    elif operator == 'LTE':
        return a <= b