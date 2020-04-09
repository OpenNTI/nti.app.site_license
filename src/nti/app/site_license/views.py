#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from pyramid import httpexceptions as hexc

from pyramid.threadlocal import get_current_request

from pyramid.view import view_config

from nti.app.externalization.error import raise_json_error

from nti.appserver.dataserver_pyramid_views import GenericGetView

from nti.externalization.interfaces import StandardExternalFields

from nti.site_license.interfaces import ISiteLicense

ITEMS = StandardExternalFields.ITEMS
TOTAL = StandardExternalFields.TOTAL
ITEM_COUNT = StandardExternalFields.ITEM_COUNT

logger = __import__('logging').getLogger(__name__)


def raise_error(data, tb=None,
                factory=hexc.HTTPUnprocessableEntity,
                request=None):
    request = request or get_current_request()
    raise_json_error(request, factory, data, tb)


@view_config(context=ISiteLicense)
class SiteLicenseView(GenericGetView):
    pass

