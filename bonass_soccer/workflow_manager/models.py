# workflow_manager/models.py
import yaml
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class Workflow(models.Model):
    name = models.CharField(max_length=255)
    yaml_config = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        try:
            self.parse_yaml()
        except Exception as e:
            raise ValidationError(f"Invalid YAML format: {str(e)}")

    def parse_yaml(self):
        config = yaml.safe_load(self.yaml_config)

        # Validate required fields
        if not config.get('name'):
            raise ValidationError("Workflow name is required")

        if not config.get('on'):
            raise ValidationError("Trigger events are required")

        return config

    def __str__(self):
        return self.name


class UserWorkflow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    tasks = models.ManyToManyField('WorkflowTask', through='TaskInstance')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)


class WorkflowTask(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    task_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    schedule = models.CharField(max_length=50)  # cron syntax
    command = models.TextField()
    depends_on = models.ManyToManyField('self', symmetrical=False, blank=True)
    timeout = models.PositiveIntegerField(default=3600)  # seconds
    retries = models.PositiveIntegerField(default=0)
    enabled = models.BooleanField(default=True)


class TaskInstance(models.Model):
    user_workflow = models.ForeignKey(UserWorkflow, on_delete=models.CASCADE)
    task = models.ForeignKey(WorkflowTask, on_delete=models.CASCADE)
    celery_task_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('scheduled', 'Scheduled'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_for = models.DateTimeField()
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)