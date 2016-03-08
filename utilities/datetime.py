from django.utils import timezone
from django.conf import settings
import pytz


def getToday():
    return pytz.timezone(settings.TIME_ZONE).normalize(timezone.now()).date()


def getNow():
    return pytz.timezone(settings.TIME_ZONE).normalize(timezone.now())
