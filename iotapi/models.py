from django.db import models
from sysmoon.models.devices import GeoLocatedMonitoringDevice


# Create your models here.
class IOTDevice(GeoLocatedMonitoringDevice):
    # TODO: Define fields here

    class Meta(object):
        verbose_name = "IoT Device"
        verbose_name_plural = "IoT Devices"
        abstract = False

    def save(self):
        return super(IOTDevice, self).save()
