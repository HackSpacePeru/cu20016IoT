from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from sysmoon.models.devices import GeoLocatedMonitoringDevice
from sysmoon.models.records import BaseRecord
from sysmoon.fields.measurements import MeasurementField


# Create your models here.
class IOTDevice(GeoLocatedMonitoringDevice):
    # TODO: Define fields here
    owner = models.ForeignKey(
        User,
        default=None,
        on_delete=models.PROTECT,
        related_name="devices",
        related_query_name="owner",
        verbose_name=_("owner"),
    )

    class Meta(object):
        verbose_name = "IoT Device"
        verbose_name_plural = "IoT Devices"
        abstract = False

    def save(self):
        return super(IOTDevice, self).save()


class IOTRecord(BaseRecord):
    device = models.ForeignKey(
        IOTDevice,
        default=None,
        on_delete=models.PROTECT,
        related_name="records",
        related_query_name="devices",
        verbose_name=_("device"),
    )

    temperature = MeasurementField(
        _("Temperature"),
        default=-9999.9999,
        null=True
    )

    class Meta(object):
        verbose_name = "IoT Record"
        verbose_name_plural = "IoT Records"
        abstract = False

    def save(self):
        return super(IOTRecord, self).save()
