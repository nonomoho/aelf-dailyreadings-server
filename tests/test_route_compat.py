# -*- coding: utf-8 -*-

import os
import server
import keys
import mock
from bs4 import BeautifulSoup

from base import TestBase, FakeResponse

class TestRouteCompat(TestBase):
    def tearDown(self):
        FakeResponse.status_code = 200

    @mock.patch('utils.requests.Session.get')
    def test_error_handling(self, m_get):
        m_get.side_effect = self.m_get

        # Nominal, should return 200
        resp = self.app.get('/19/office/complies/2016-05-23?beta=enabled')
        self.assertEqual(200, resp.status_code)

        # 404
        FakeResponse.status_code = 404
        resp = self.app.get('/19/office/complies/2016-05-23?beta=enabled')
        self.assertEqual(404, resp.status_code)

        # Teapot
        FakeResponse.status_code = 419
        resp = self.app.get('/19/office/complies/2016-05-23?beta=enabled')
        self.assertEqual(419, resp.status_code)

    @mock.patch('server.do_get_office')
    def test_get_meta(self, m_do_get_office):
        def mock_get_office(*args):
            return "OK"
        m_do_get_office.side_effect = mock_get_office

        # Test: key to office translation
        for office, key in keys.KEYS.iteritems():
            self.assertEqual("OK", self.app.get('/01/02/2016/'+key).data)
            m_do_get_office.assert_called_once_with(0, office, 1, 2, 2016)
            m_do_get_office.reset_mock()

        # Test: version+beta forwarding
        self.assertEqual("OK", self.app.get('/01/02/2016/'+key+'?version=19&beta=1').data)
        m_do_get_office.assert_called_once_with(19, office, 1, 2, 2016)
        m_do_get_office.reset_mock()


