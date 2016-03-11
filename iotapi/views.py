from django.http import HttpResponse
from django.views.generic import TemplateView

# import datetime
import json


class APIView(TemplateView):

    def get(self, request, *args, **kwargs):
        response_dict = {
            "Holi": "boli",
        }

        response = json.dumps(response_dict, indent=4, sort_keys=True)

        return HttpResponse(response, content_type="application/json")
