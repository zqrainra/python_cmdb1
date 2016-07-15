#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Bob'
from models import CPU,RAM
from rest_framework import serializers

class CPUSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPU
        fields = ('asset', 'cpu_model', 'cpu_count')


class RAMSerializer(serializers.ModelSerializer):
    class Meta:
        model = RAM
        fields = ('asset','model')