from django.contrib import admin

from sysmoon.admin import GeoLocatedMonitoringDeviceBaseAdmin
from sysmoon.admin import BaseRecordBaseAdmin

from iotapi.models import IOTDevice
from iotapi.models import IOTRecord


@admin.register(IOTDevice)
class IOTDeviceAdmin(GeoLocatedMonitoringDeviceBaseAdmin):
    model = IOTDevice

    list_display = (
        "code",
        "status",
        "begin_of_service",
        "end_of_service",
        "latitude",
        "longitude",
        "elevation"
    )

    radio_fields = {"status": admin.VERTICAL}

    def get_fields(self, request, obj=None):
        if obj is not None:
            if obj.status == obj.STATUS_OUT_OF_SERVICE:
                return ("code", "owner", "status", "registration_date", "begin_of_service", "end_of_service", "position")

            return ("code", "owner", "status", "registration_date", "begin_of_service", "position")

        return ("code", "owner", "status", "begin_of_service", "position")

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ["code", ]

        if obj:
            readonly_fields = [
                "code",
                "begin_of_service",
                "registration_date",
            ]

            if obj.status == obj.STATUS_OUT_OF_SERVICE:
                readonly_fields = [
                    "code",
                    "owner",
                    "registration_date",
                    "begin_of_service",
                    "end_of_service",
                    "position",
                ]

        return readonly_fields


@admin.register(IOTRecord)
class IOTRecordAdmin(BaseRecordBaseAdmin):
    model = IOTRecord

    list_display = (
        "device",
        "log_date",
        "temperature"
    )
