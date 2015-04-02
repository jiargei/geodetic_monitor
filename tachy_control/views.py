from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework import permissions

from tachy_control.models import TachySensor
from tachy_control.serializers import TachySensorSerializer
from tachy_control.lib.sensors import TACHY_FACTORY

import random
import serial

# Create your views here.

class TachySensorViewSet(viewsets.ModelViewSet):
    """
    This vieset automatically provides 'list', 'create', 'retrieve',
    'update' and 'destroy' actions.

    Additionally we also provide:

    - 'angles'
    - 'get_distance'
    - 'get_instrument_name'
    - 'get_instrument_number'

    """
    queryset = TachySensor.objects.all()
    serializer_class = TachySensorSerializer

    def percorm_create(self, serializer):
        serializer.save(owner=self.request.user)

    def init_tachy(self, model, device, baudrate, 
                   bytesize, stopbits, parity, address):
        """
        """
        tachy_factory = TACHY_FACTORY.TachyFactory(baudrate, bytesize, 
                                                   stopbits, device, 
                                                   address, parity)
        return tachy_factory.new_tachy(tachy_type=model)

    def getter(self, request, method):
        sensor = self.get_object()
        serializer = TachySensorSerializer(data=request.data)
        tachy_serial = self.init_tachy(sensor.model,
                                       sensor.device,
                                       sensor.baudrate,
                                       sensor.bytesize,
                                       sensor.stopbits,
                                       sensor.parity,
                                       sensor.address)
        tachy_out = eval('tachy_serial.%s' % method)
        tachy_serial.disconnect()
        if tachy_out == {}:
            return Response({'detail': 'no data from tachy sensor'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(tachy_out,
                        status=status.HTTP_200_OK)

    @detail_route()
    def angles(self, request, pk=None):
        return self.getter(request, "get_angles(True)")

    @detail_route()
    def get_distance(self, request, pk=None):
        return self.getter(request, "get_slope_distance()")

    @detail_route()
    def get_instrument_name(self, request, pk=None):
        return self.getter(request, "get_instrument_name()")

    @detail_route()
    def get_instrument_number(self, request, pk=None):
        return self.getter(request, "get_instrument_number()")
