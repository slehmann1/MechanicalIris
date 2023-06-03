from django.contrib.auth.models import Group, User
from django.http.response import HttpResponse
from rest_framework import permissions
from rest_framework import views as REST_Views
from rest_framework import viewsets
from rest_framework.response import Response

from iris_calculator.iris import Iris
from iris_calculator.serializers import GroupSerializer, IrisSerializer, UserSerializer

# Create your views here.


class IrisView(REST_Views.APIView):
    def post(self, request):
        print("Recieved Request:")
        print(request.data)
        iris = Iris(
            int(request.data["bladeCount"]),
            request.data["minDiameter"] / 2,
            request.data["maxDiameter"] / 2,
            request.data["bladeWidth"],
            request.data["pinRadius"],
            request.data["pinClearance"],
        )
        iris = IrisSerializer(
            {
                "blade_radius": iris.blades[0].blade_radius,
                "pinned_radius": iris.blades[0].pinned_radius,
                "min_angle": iris.domain[0],
                "max_angle": iris.domain[1],
                "bc": iris.BC,
            }
        )
        results = iris.data
        return Response(results)


class DXFView(REST_Views.APIView):
    def get(self, request):
        print("Recieved DXF Request")
        iris = Iris(
            int(request.GET.get("bladeCount")),
            float(request.GET.get("minDiameter")) / 2,
            float(request.GET.get("maxDiameter")) / 2,
            float(request.GET.get("bladeWidth")),
            float(request.GET.get("pinRadius")),
            float(request.GET.get("pinClearance")),
        )

        zip = iris.save_dxfs_as_zip()
        response = HttpResponse(zip, content_type="application/zip")
        response["Content-Disposition"] = "attachment; filename=name.zip"
        return response
