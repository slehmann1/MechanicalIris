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
    def get(self, request):
        print("Recieved Request:")
        print(request.data)
        iris = Iris(
            int(request.GET.get("bladeCount")),
            float(request.GET.get("minDiameter")) / 2,
            float(request.GET.get("maxDiameter")) / 2,
            float(request.GET.get("bladeWidth")),
            float(request.GET.get("pinRadius")),
            float(request.GET.get("pinClearance")),
        )
        a_coords = iris.get_A_coords()
        iris = IrisSerializer(
            {
                "blade_radius": iris.blades[0].blade_radius,
                "pinned_radius": iris.blades[0].pinned_radius,
                "min_angle": iris.get_actuator_rotation_range()[0],
                "max_angle": iris.get_actuator_rotation_range()[1],
                "bc": iris.BC,
                "slot_inner_radius": iris.actuator_ring.get_slot_inner_radius(),
                "slot_outer_radius": iris.actuator_ring.get_slot_outer_radius(),
                "a_coords": a_coords,
                "actuator_ring_angle": iris.blade_states[0][0].A.angle(),
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
