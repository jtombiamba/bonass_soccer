# workflow_manager/tasks.py
from celery import shared_task
from celery.schedules import crontab
from django.utils import timezone
from .models import UserWorkflow, WorkflowTask, TaskInstance
from datetime import timedelta


@shared_task
def execute_workflow_task(task_instance_id):
    task_instance = TaskInstance.objects.get(id=task_instance_id)
    try:
        task_instance.status = 'running'
        task_instance.started_at = timezone.now()
        task_instance.save()

        # Execute your command here (e.g., subprocess, API call, etc.)
        # result = execute_command(task_instance.task.command)

        task_instance.status = 'completed'
        task_instance.completed_at = timezone.now()
        task_instance.save()

    except Exception as e:
        task_instance.status = 'failed'
        task_instance.save()
        raise


def schedule_workflow_tasks(user_workflow_id):
    user_workflow = UserWorkflow.objects.get(id=user_workflow_id)
    workflow = user_workflow.workflow
    config = workflow.parse_yaml()

    for task_config in config.get('jobs', []):
        task = WorkflowTask.objects.get(workflow=workflow, task_id=task_config['id'])

        # Calculate first run time based on schedule
        # (Implement cron parser or use celery beat schedule)
        scheduled_time = timezone.now() + timedelta(minutes=5)

        task_instance = TaskInstance.objects.create(
            user_workflow=user_workflow,
            task=task,
            scheduled_for=scheduled_time,
            status='scheduled'
        )

        # Schedule Celery task
        result = execute_workflow_task.apply_async(
            args=[task_instance.id],
            eta=scheduled_time
        )
        task_instance.celery_task_id = result.id
        task_instance.save()