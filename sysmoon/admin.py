from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# Section 0:
#   Importable Objects
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
__all__ = [
    'GeoLocatedMonitoringDeviceBaseAdmin',
    'MonitoringDeviceBaseAdmin',
    'BaseRecordBaseAdmin',
]


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# Section 1:
#   Monitoring Devices Registration
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

class MonitoringDeviceBaseAdmin(admin.ModelAdmin):
    def registration_date_(self, obj):
        return obj.registration_date_

    registration_date_.short_description = _("registration date")
    registration_date_.admin_order_field = "registration_date"

    def begin_of_service_(self, obj):
        return obj.begin_of_service_

    begin_of_service_.short_description = _("begin of service")
    begin_of_service_.admin_order_field = "begin_of_service"

    def end_of_service_(self, obj):
        return obj.end_of_service_

    end_of_service_.short_description = _("end of service")
    end_of_service_.admin_order_field = "end_of_service"

    def code(self, obj):
        return obj.code

    code.short_description = _("station code")
    code.admin_order_field = "pk"


class GeoLocatedMonitoringDeviceBaseAdmin(MonitoringDeviceBaseAdmin):
    def latitude(self, obj):
        return obj.latitude

    latitude.short_description = _("latitude")

    def longitude(self, obj):
        return obj.longitude

    longitude.short_description = _("longitude")

    def elevation(self, obj):
        return obj.elevation

    elevation.short_description = _("elevation")


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# Section 2:
#   Monitoring Records Registration
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
class BaseRecordBaseAdmin(admin.ModelAdmin):
    def log_date_(self, obj):
        return obj.log_date_

    log_date_.short_description = _("log date")
    log_date_.admin_order_field = "log_date"
