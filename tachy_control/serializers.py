from django.forms import widgets
from rest_framework import serializers

from tachy_control.models import TachySensor

class TachySensorSerializer(serializers.HyperlinkedModelSerializer):   
    owner = serializers.ReadOnlyField(source='owner.username') 
    class Meta:
        model = TachySensor
        fields = ('owner', 'instrument_name', 'instrument_number', 'model', 'device',
                  'baudrate', 'bytesize', 'stopbits', 'parity')
