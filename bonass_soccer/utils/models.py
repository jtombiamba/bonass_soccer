import uuid

from django.db.models import DateTimeField
from django.db.models import Model
from django.db.models import UUIDField
from django.utils.translation import gettext_lazy as _


class AbstractUUIDModel(Model):
    uuid = UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class AbstractTimestampedModel(Model):
    created = DateTimeField(_("Creation date"), auto_now_add=True)
    modified = DateTimeField(_("Last update"), auto_now=True)

    class Meta:
        abstract = True


class AbstractBaseModel(
    AbstractUUIDModel,
    AbstractTimestampedModel,
):
    class Meta:
        abstract = True
