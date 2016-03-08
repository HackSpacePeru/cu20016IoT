from django.db import models
from django.utils.translation import ugettext_lazy as _

import uuid


class UUIDBaseModel(models.Model):

    """
    Base clase for objects with ID given by uuid4 algorithm
    """

    id = models.UUIDField(
        _("Identification Code"),
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )

    class Meta:
        verbose_name = "UUID base model"
        verbose_name_plural = "UUID base models"
        abstract = True

    def save(self, *args, **kwargs):
        super(UUIDBaseModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.id
