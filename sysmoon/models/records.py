from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from inspect import getmro

from .devices import MonitoringDevice


class BaseRecord(models.Model):

    """
        Base class for records with basic functionality for bad data, record status and dates.

        Fields:
    """

    device = None

    STATUS_FULLY = 1
    STATUS_EMPTY = 0
    STATUS_LOSSY = -1

    STATUS_MAP = (
        (STATUS_FULLY, _("Complete record")),
        (STATUS_EMPTY, _("Empty record")),
        (STATUS_LOSSY, _("Loosy record")),
    )

    status = models.IntegerField(
        _("record status"),
        choices=STATUS_MAP,
        default=STATUS_EMPTY
    )

    log_date = models.DateTimeField(
        _("log date"),
        default=timezone.now,
        help_text=_('Please introduce the log time as UTC time.')
    )

    @property
    def log_date_(self):
        if self.log_date:
            return self.log_date.strftime("%Y-%m-%dT%H:%M:%S+00:00")

        return ''

    log_date_.fget.short_description = _("log date")
    log_date_.fget.admin_order_field = "log_date"

    class Meta:
        verbose_name = _("base record")
        verbose_name_plural = _("base record")
        abstract = True

    def clean(self):
        if self.device:
            if MonitoringDevice in getmro(type(self.device)):
                errorDict = {}

                if self.log_date and self.device.begin_of_service:
                    if self.log_date.date() < self.device.begin_of_service:
                        errorDict.update({
                            'log_date': ValidationError(_('Log date can\'t be before the begin of service fo the device')),
                        })

                if self.device.end_of_service and self.log_date:
                    if self.device.begin_of_service < self.log_date.date():
                        errorDict.update({
                            'log_date': ValidationError(_('Log date can\'t be after the end of service fo the device')),
                        })

                if errorDict:
                    raise ValidationError(errorDict)
