#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test specifically for the `punycode` function."""

import unittest

from ioc_toolkit import ioc_toolkit


class LegacyPunycodeAPITestCase(unittest.TestCase):
    """Test for legacy API endpoint."""

    def setUp(self):
        self.app = ioc_toolkit.app.test_client()

    def test_api(self):
        """Test out the punycode conversion api - this is a legacy feature."""
        rv = self.app.post('/api/v1/convert?from=punycode&to=unicode', data={'domain': 'xn--l3h.com'})
        self.assertIn('☁.com', rv.data.decode())
        rv = self.app.post('/api/v1/convert?from=punycode&to=unicode', data={'domain': 'xn--fng.com'})
        self.assertIn('ἂ.com', rv.data.decode())
        rv = self.app.post('/api/v1/convert?from=punycode&to=unicode', data={'domain': 'xn--80a.com'})
        self.assertIn('а.com', rv.data.decode())


class PunycodeUITests(unittest.TestCase):

    def setUp(self):
        self.app = ioc_toolkit.app.test_client()
        self.base_url = '/punycode'

    def test_encode(self):
        rv = self.app.get(self.base_url + '?text=點看&action=Decode')
        assert 'xn--c1yn36f' in rv.data.decode()
        assert '點看' in rv.data.decode()

    def test_decode(self):
        rv = self.app.get(self.base_url + '?text=xn--c1yn36f&action=Encode')
        assert '點看' in rv.data.decode()
        assert 'xn--c1yn36f' in rv.data.decode()


class PunycodeAPITests(unittest.TestCase):

    def setUp(self):
        self.app = ioc_toolkit.app.test_client()
        self.base_url = '/api/v1/punycode'

    def test_decode(self):
        rv = self.app.post(self.base_url, data={
            'text': '點看',
            'action': 'decode'
        })
        self.assertIn('xn--c1yn36f', rv.data.decode())

    def test_encode(self):
        rv = self.app.post(self.base_url, data={
            'text': 'xn--c1yn36f',
            'action': 'encode'
        })
        self.assertIn('點看', rv.data.decode())
