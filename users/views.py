from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import status
from rest_framework import permissions

from django.contrib.auth.models import User

from users.serializers import UserSerializer

# Create your views here.


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides 'list' and 'detail' actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
