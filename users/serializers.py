from django.forms import widgets
from django.contrib.auth.models import User

from rest_framework import serializers

from setup.models import Project
from tachy_control.models import TachySensor

class UserSerializer(serializers.ModelSerializer):
    projects = serializers.PrimaryKeyRelatedField(many=True, queryset=Project.objects.all())
    tachysensors = serializers.PrimaryKeyRelatedField(many=True, queryset=TachySensor.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'projects', 'tachysensors', )
