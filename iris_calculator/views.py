from django.contrib.auth.models import Group, User
from rest_framework import permissions
from rest_framework import views as REST_Views
from rest_framework import viewsets
from rest_framework.response import Response

from iris_calculator.serializers import GroupSerializer, IrisSerializer, UserSerializer

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class IrisView(REST_Views.APIView):
    def post(self, request):
        print("Recieved Request:")
        print(request.data)
        iris = IrisSerializer(
            {
                "blade_radius": 1,
                "pinned_radius": 2,
                "min_angle": 3,
                "max_angle": 4,
                "bc": 5,
            }
        )
        results = iris.data
        return Response(results)
