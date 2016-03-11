from django.conf.urls import url
from django.contrib import admin

from iotapi.views import APIView

urlpatterns = [
    url(r'^dummy/', APIView.as_view(), name="dummy")
]
