# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from apps.home.models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Blog)
admin.site.register(BlogSection)
