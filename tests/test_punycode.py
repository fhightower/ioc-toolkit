#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from ioc_toolkit import ioc_toolkit


class PunycodeDecoderTestCase(unittest.TestCase):

    def setUp(self):
        self.app = ioc_toolkit.app.test_client()

    def test_ui(self):
        # rv = self.app.get('/punycode')
        # self.assertIn('punycode', rv.data.decode())
        pass

    def test_api(self):
        """Test out the punycode conversion api - this is a legacy feature."""
        rv = self.app.post('/api/v1/convert?from=punycode&to=unicode', data={'domain': 'xn--l3h.com'})
        self.assertIn('☁.com', rv.data.decode())
        rv = self.app.post('/api/v1/convert?from=punycode&to=unicode', data={'domain': 'xn--fng.com'})
        self.assertIn('ἂ.com', rv.data.decode())
        rv = self.app.post('/api/v1/convert?from=punycode&to=unicode', data={'domain': 'xn--80a.com'})
        self.assertIn('а.com', rv.data.decode())
