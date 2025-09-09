from bonass_soccer.workflow_manager.models import Workflow, UserWorkflow


def create_workflow():
    yaml_config = """
    name: Example Workflow
    on:
      user_join: true
    jobs:
      task1:
        name: Initial Setup
        schedule: "every 10 minutes"
        command: "echo 'Running setup'"
    """

    workflow = Workflow.objects.create(
        name="Example Workflow",
        yaml_config=yaml_config
    )
    workflow.parse_yaml()  # Validates YAML


def start_workflow_for_user():
    user_workflow = UserWorkflow.objects.create(
        user=request.user,
        workflow=workflow,
        status='running'
    )
    schedule_workflow_tasks.delay(user_workflow.id)