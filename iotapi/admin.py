from django.contrib import admin

from sysmoon.admin import GeoLocatedMonitoringDeviceBaseAdmin
from iotapi.models import IOTDevice


@admin.register(IOTDevice)
class IOTDeviceAdmin(GeoLocatedMonitoringDeviceBaseAdmin):
    model = IOTDevice
