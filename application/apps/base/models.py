import uuid

from django.db import models


class StandardModelMixin(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Id")

    create_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at"
    )

    write_date = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated at"
    )

    class Meta:
        abstract = True
