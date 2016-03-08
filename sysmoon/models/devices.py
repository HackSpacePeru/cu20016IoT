from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from geoposition import fields as gmodels


class MonitoringDevice(models.Model):

    """
        Base clase to construct monitoring device models.

        Properties (overridable):
          * code_prefix:
            - Data type: string
            - Description: Unique identification code prefix to identify monitoring devices. Field to override in derived models.

          * code:
            - Data type: string
            - Description: Unique identification code for station. Is compound by the code prefix and the devie id.
            - Note: Defined as property.

          * status:
            - Data type: integer
            - Description: Indicates wherter the monitoring device in service, out of services or under maintian. Check this field as out of service instead of delete the device.

          * registration_date:
            - Data type: datetime
            - Description: Indicates the date and hour when the station was registered.

          * end_of_service:
            - Data type: datetime
            - Description: Indicates the date and hour when the station status was setted to "out of service".
    """

    STATUS_IN_SERVICE = 1
    STATUS_IN_MAINTENANCE = 0
    STATUS_OUT_OF_SERVICE = -1

    STATUS_MAP = (
        (STATUS_IN_SERVICE, _("In service")),
        (STATUS_IN_MAINTENANCE, _("In maintenance")),
        (STATUS_OUT_OF_SERVICE, _("Out of service")),
    )

    status = models.IntegerField(
        _("device status"),
        choices=STATUS_MAP,
        default=STATUS_IN_SERVICE,
        help_text=_(
            "Designates whether this monitoring device should be treated "
            "as active. Set this to \"out of service\" instead of deleting device."
        )
    )

    registration_date = models.DateTimeField(
        _("registration date"),
        default=timezone.now,
        editable=False,
    )

    begin_of_service = models.DateField(
        _("begin of service"),
        default=timezone.now,
    )

    end_of_service = models.DateField(
        _("end of service"),
        null=True,
        blank=True,
        default=None,
    )

    @property
    def registration_date_(self):
        if self.registration_date is None:
            return ''

        return self.registration_date.strftime("%Y-%m-%dT%H:%M:%S+00:00")

    @property
    def begin_of_service_(self):
        if self.begin_of_service is None:
            return ''

        return self.begin_of_service.strftime("%Y-%m-%dT%H:%M:%S+00:00")

    @property
    def end_of_service_(self):
        if self.end_of_service is None:
            return ''

        return self.end_of_service.strftime("%Y-%m-%dT%H:%M:%S+00:00")

    code_prefix = "MD"

    @property
    def code(self):
        if self.pk is None:
            return self.code_prefix + 6 * "X"

        return "{0:}{1:0>6d}".format(self.code_prefix, self.pk)

    class Meta:
        verbose_name = _("monitoring device")
        verbose_name_plural = _("monitoring devices")
        abstract = True

    def save(self, *args, **kargs):
        if self.pk is None:
            self.registration_date = timezone.now()
            old_status = self.STATUS_IN_SERVICE

        if self.pk is not None:
            old_status = type(self).objects.get(pk=self.pk).status

        if self.status == self.STATUS_OUT_OF_SERVICE and self.status != old_status:
            self.end_of_service = timezone.now()
        else:
            self.end_of_service = None

        if self.end_of_service:
            self.status = self.STATUS_OUT_OF_SERVICE

        return super(MonitoringDevice, self).save(*args, **kargs)

    def clean(self):
        errorDict = {}

        if self.registration_date and self.begin_of_service:
            if self.registration_date.date() < self.begin_of_service:
                errorDict.update({
                    'begin_of_service': ValidationError(_('Begin of service can\'t be after registrations date'), code='required'),
                })

        if self.end_of_service and self.begin_of_service:
            if self.end_of_service < self.begin_of_service:
                errorDict.update({
                    'end_of_service': ValidationError(_('End of service can\'t be before registrations date'), code='required'),
                })

        if errorDict:
            raise ValidationError(errorDict)

        return super(MonitoringDevice, self).clean()

    def __str__(self):
        return self.code


class GeoLocatedMonitoringDevice(MonitoringDevice):

    """
        Base clase for construct models for geolocated monitorig devices.

        Fields:
          * code_prefix:
            - Data type: string
            - Description: Unique identification code prefix to identify monitoring devices. Field to override in derived models.
            - Note: Overridable.

          * code:
            - Data type: string
            - Description: Unique identification code for station. Is compound by the code prefix and the devie id.
            - Note: Defined as property.

          * status:
            - Data type: integer
            - Description: Indicates wherter the monitoring device in service, out of services or under maintian. Check this field as out of service instead of delete the device.

          * registration_date:
            - Data type: datetime
            - Description: Indicates the date and hour when the station was registered.

          * end_of_service:
            - Data type: datetime
            - Description: Indicates the date and hour when the station status was setted to "out of service".

          * position:
            - Data type: compound (geolocation object)
            - Description: Indicates the geographical position (latitude, longitude, altitude) of a monitoring device.

          * latitude:
            - Data type: float
            - Description: Indicates the latitude of the monitoring device.
            - Note: Defined as property.

          * longitude:
            - Data type: float
            - Description: Indicates the longitude of the monitoring device.
            - Note: Defined as property.

          * elevation:
            - Data type: float
            - Description: Indicates the elevation of the monitoring device.
            - Note: Defined as property.
    """

    code_prefix = "GMD"

    position = gmodels.GeopositionField(
        _("position")
    )

    @property
    def latitude(self):
        lat = self.position.latitude
        orientation = "N" if lat > 0 else "S" if lat < 0 else ""
        lat = abs(lat)
        deg = int(lat)
        lat = 60 * (lat - deg)
        min = int(lat)
        lat = 60 * (lat - min)
        sec = lat

        return "{0:}°{1:0>2d}'{2:0>9.6f}''{3:}".format(deg, min, sec, orientation)

    @property
    def longitude(self):
        lng = self.position.longitude
        orientation = "E" if lng > 0 else "W" if lng < 0 else ""
        lng = abs(lng)
        deg = int(lng)
        lng = 60 * (lng - deg)
        min = int(lng)
        lng = 60 * (lng - min)
        sec = lng

        return "{0:}°{1:0>2d}'{2:0>9.6f}''{3:}".format(deg, min, sec, orientation)

    @property
    def elevation(self):
        return "{0:.3f} m".format(self.position.elevation)

    class Meta:
        verbose_name = _("geolocated monitoring device")
        verbose_name_plural = _("geolocated monitoring devices")
        abstract = True
