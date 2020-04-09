#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import component
from zope import interface

from nti.dataserver.authorization_acl import acl_from_aces
from nti.dataserver.authorization_acl import ace_denying_all

from nti.dataserver.interfaces import IACLProvider

from nti.site_license.interfaces import ISiteLicense

logger = __import__('logging').getLogger(__name__)


@interface.implementer(IACLProvider)
@component.adapter(ISiteLicense)
class SiteLicenseACLProvider(object):

    def __init__(self, context):
        self.context = context

    @property
    def __parent__(self):
        return self.context.__parent__

    @property
    def __acl__(self):
        # Admins get their perms from zope world
        acl = [ace_denying_all()]
        result = acl_from_aces(acl)
        return result
