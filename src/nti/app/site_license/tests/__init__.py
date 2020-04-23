#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import unittest

import zope.testing.cleanup

from nti.app.testing.application_webtest import ApplicationLayerTest
from nti.app.testing.application_webtest import ApplicationTestLayer

from nti.testing.base import AbstractTestBase

from nti.testing.layers import ZopeComponentLayer
from nti.testing.layers import ConfiguringLayerMixin


class SharedConfiguringTestLayer(ApplicationTestLayer):

    set_up_packages = ('nti.app.site_license',)

    @classmethod
    def setUp(cls):
        cls.setUpPackages()

    @classmethod
    def tearDown(cls):
        cls.tearDownPackages()
        zope.testing.cleanup.cleanUp()

    @classmethod
    def testSetUp(cls):
        pass

    @classmethod
    def testTearDown(cls):
        pass


class SiteLayerTest(ApplicationLayerTest):

    layer = SharedConfiguringTestLayer
