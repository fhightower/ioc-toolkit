#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test specifically for the `url_encode_decode` function."""

import unittest

from ioc_toolkit import ioc_toolkit


class UrlEncodeDecodeUITests(unittest.TestCase):

    def setUp(self):
        self.app = ioc_toolkit.app.test_client()
        self.base_url = '/url-encode-decode'

    def test_encode(self):
        rv = self.app.get(self.base_url + '?text=test%3D20*2&action=Encode')
        assert 'test%3D20%2A2' in rv.data.decode()
        assert 'test=20*2' in rv.data.decode()

    def test_decode(self):
        rv = self.app.get(self.base_url + '?text=test%253D20%252A2&action=Decode')
        assert 'test=20*2' in rv.data.decode()
        assert 'test%3D20%2A2' in rv.data.decode()


class UrlEncodeDecodeAPITests(unittest.TestCase):

    def setUp(self):
        self.app = ioc_toolkit.app.test_client()
        self.base_url = '/api/v1/url-encode-decode'

    def test_decode(self):
        rv = self.app.post(self.base_url, data={
            'text': 'test%3D20%2A2',
            'action': 'decode'
        })
        self.assertIn('test=20*2', rv.data.decode())

    def test_encode(self):
        rv = self.app.post(self.base_url, data={
            'text': 'test=20*2',
            'action': 'encode'
        })
        self.assertIn('test%3D20%2A2', rv.data.decode())
