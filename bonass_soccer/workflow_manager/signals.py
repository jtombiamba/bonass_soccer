# workflow_manager/signals.py
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import UserWorkflow, TaskInstance
from celery.result import AsyncResult

@receiver(pre_save, sender=UserWorkflow)
def handle_workflow_status_change(sender, instance, **kwargs):
    if instance.pk:
        original = UserWorkflow.objects.get(pk=instance.pk)
        if original.status != instance.status and instance.status == 'cancelled':
            # Cancel all scheduled tasks
            for task_instance in instance.taskinstance_set.filter(status__in=['pending', 'scheduled']):
                if task_instance.celery_task_id:
                    AsyncResult(task_instance.celery_task_id).revoke(terminate=True)
                task_instance.status = 'cancelled'
                task_instance.save()