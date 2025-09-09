// conditions.js
document.addEventListener('DOMContentLoaded', () => {
  // Initialize visibility
  updateQuestionVisibility();

  // Listen to all input changes
  document.querySelectorAll('input, select').forEach(input => {
    input.addEventListener('change', () => {
      updateQuestionVisibility();
    });
  });
});

async function updateQuestionVisibility() {
  // Get current answers
  const formData = new FormData(document.getElementById('dynamic-form'));

  // Fetch conditions from backend (preloaded in data attributes)
  document.querySelectorAll('.question[data-conditions]').forEach(questionEl => {
    const conditions = JSON.parse(questionEl.dataset.conditions);
    let shouldShow = false;

    conditions.forEach(conditionGroup => {
      let groupResult = true;

      conditionGroup.clauses.forEach(clause => {
        const answerValue = formData.get(`q${clause.source_question_id}`);
        groupResult = groupResult && evaluateClause(answerValue, clause);
      });

      shouldShow = shouldShow || groupResult;
    });

    questionEl.style.display = shouldShow ? 'block' : 'none';
  });
}

function evaluateClause(answerValue, clause) {
  // Implement comparison logic based on clause.operator
  // Example:
  if (clause.operator === 'EQUALS') {
    return answerValue == clause.expected_value;
  }
  // Add other operators...
}