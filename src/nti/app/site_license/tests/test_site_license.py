#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from hamcrest import is_
from hamcrest import none
from hamcrest import not_none
from hamcrest import assert_that
from hamcrest import has_entries

from zope.component.hooks import getSite

from zope.securitypolicy.interfaces import IPrincipalRoleManager

from nti.app.site_license import VIEW_SITE_LICENSE

from nti.app.site.tests import SiteLayerTest

from nti.app.testing.decorators import WithSharedApplicationMockDS

from nti.dataserver.authorization import ROLE_SITE_ADMIN_NAME

from nti.dataserver.tests import mock_dataserver

logger = __import__('logging').getLogger(__name__)


class TestSiteLicense(SiteLayerTest):

    default_origin = 'https://test_site_license'

    def _get_workspace(self, name, environ, exists=True):
        service_res = self.testapp.get('/dataserver2',
                                       extra_environ=environ)
        service_res = service_res.json_body
        workspaces = service_res['Items']
        result = None
        try:
            result = next(x for x in workspaces if x['Title'] == name)
        except StopIteration:
            pass
        to_check = not_none if exists else none
        assert_that(result, to_check())
        return result

    @WithSharedApplicationMockDS(testapp=True, users=True)
    def test_site_license(self):
        """
        Validate site license api and workspace rels.
        """

        # Make a site admin user
        with mock_dataserver.mock_db_trans(self.ds, site_name='test_site_license'):
            self._create_user(u'sitelicense_siteadmin', u'temp001',
                              external_value={'realname': u'Site License',
                                              'email': u'sitelicense@test.com'})
            self._create_user(u'sitelicense_regularuser', u'temp001',
                              external_value={'realname': u'Site License',
                                              'email': u'sitelicense@test.com'})
            new_site = getSite()
            prm = IPrincipalRoleManager(new_site)
            prm.assignRoleToPrincipal(ROLE_SITE_ADMIN_NAME,
                                      u'sitelicense_siteadmin')

        # Update rel
        site_admin_env = self._make_extra_environ('sitelicense_siteadmin')
        regular_env = self._make_extra_environ('sitelicense_regularuser')
        site_admin_ws = self._get_workspace('SiteAdmin',
                                            site_admin_env)
        license_rel = self.require_link_href_with_rel(site_admin_ws,
                                                      VIEW_SITE_LICENSE)

#         license_res = self.testapp.get(license_rel, extra_environ=site_admin_env)
#         license_res = license_res.json_body
#         brand_href = license_res.get('href')
#         assert_that(brand_href, not_none())
#         assert_that(license_res, has_entries('assets', none(),
#                                            'brand_name', is_('NextThought')))
#         self.require_link_href_with_rel(license_res, 'edit')
#         self.forbid_link_with_rel(license_res, 'delete')
