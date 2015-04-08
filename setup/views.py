from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from setup.models import Project
from setup.models import TachyPosition
from setup.models import TachyStation
from setup.models import FipoTarget
from setup.models import FipoTask
from setup.models import FipoMeasurement
from setup.models import SupoTarget
from setup.models import SupoTask
from setup.models import SupoMeasurement

from setup.permissions import IsOwnerOrReadOnly, IsOwner
from setup.permissions import IsReadOnly, IsOwnerOrSuperUser

from setup.serializers import ProjectSerializer
from setup.serializers import TachyPositionSerializer
from setup.serializers import TachyStationSerializer
from setup.serializers import FipoTargetSerializer
from setup.serializers import FipoTaskSerializer
from setup.serializers import FipoMeasurementSerializer
from setup.serializers import SupoTargetSerializer
from setup.serializers import SupoTaskSerializer
from setup.serializers import SupoMeasurementSerializer

import random
import serial

# Create your views here.


class ProjectViewSet(viewsets.ModelViewSet):
    """
    This vieset automatically provides 

    - 'list'
    - 'create'
    - 'retrieve'
    - 'update'
    - 'destroy' 

    actions.

    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsOwnerOrSuperUser,
                          # permissions.AllowAny,
                         )

    def get_queryset(self):
        """
        This view should return a list of all the projects
        for the currently authenticated user.
        """
        if self.request.user.is_superuser:
            return Project.objects.all()
        
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_object(self):
        obj = get_object_or_404(self.get_queryset())
        self.check_object_permissions(self.request, obj)
        return obj

    
class TachyPositionViewSet(viewsets.ModelViewSet):
    queryset = TachyPosition.objects.all()
    serializer_class = TachyPositionSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsOwner,)


class TachyStationViewSet(viewsets.ModelViewSet):
    queryset = TachyStation.objects.all()
    serializer_class = TachyStationSerializer
    permission_classes = (IsOwner,)


class FipoTargetViewSet(viewsets.ModelViewSet):
    queryset = FipoTarget.objects.all()
    serializer_class = FipoTargetSerializer
    permission_classes = (IsOwner,)


class FipoTaskViewSet(viewsets.ModelViewSet):
    queryset = FipoTask.objects.all()
    serializer_class = FipoTaskSerializer
    permission_classes = (IsOwner,)


class SupoTargetViewSet(viewsets.ModelViewSet):
    queryset = SupoTarget.objects.all()
    serializer_class = SupoTargetSerializer
    permission_classes = (IsOwner,)


class SupoTaskViewSet(viewsets.ModelViewSet):
    queryset = SupoTask.objects.all()
    serializer_class = SupoTaskSerializer
    permission_classes = (IsOwner,)


class FipoMeasurementViewSet(viewsets.ModelViewSet):
    queryset = FipoMeasurement.objects.all()
    serializer_class = FipoMeasurementSerializer
    permission_classes = (IsOwner,)

class SupoMeasurementViewSet(viewsets.ModelViewSet):
    queryset = SupoMeasurement.objects.all()
    serializer_class = SupoMeasurementSerializer
    permission_classes = (IsOwner,)
