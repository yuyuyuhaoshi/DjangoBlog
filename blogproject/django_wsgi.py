#!/usr/bin/env python
# coding: utf-8

import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogproject.settings")


from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
