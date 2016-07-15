#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Bob'

from models import CPU,RAM
from rest_framework import viewsets
from serializers import CPUSerializer,RAMSerializer


class CPUViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CPU.objects.all()
    serializer_class = CPUSerializer


class RAMViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = RAM.objects.all()
    serializer_class = RAMSerializer