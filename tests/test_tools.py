#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test specifically for the `url_encode_decode` function."""

import urllib
import unittest

from ioc_toolkit import ioc_toolkit


class ToolTester(unittest.TestCase):

    def setUp(self):
        self.app = ioc_toolkit.app.test_client()

    def test_ui(self):
        """Test the UI for each tool."""
        for tool in ioc_toolkit.tools:
            for test_action in tool['tests']:
                url = '/{}?text={}&action={}'.format(tool['uri'], tool['tests'][test_action]['input'], test_action)
                print("running tests for {}".format(url))
                rv = self.app.get(url)
                self.assertIn(tool['name'], rv.data.decode())
                self.assertIn(tool['description'], rv.data.decode())
                # it is important to unquote the input in the test below so that the url_encode_decode tests will work properly
                self.assertIn(urllib.parse.unquote(tool['tests'][test_action]['input']), rv.data.decode())
                self.assertIn(tool['tests'][test_action]['output'], rv.data.decode())

    def test_api(self):
        """Test the API for each tool."""
        for tool in ioc_toolkit.tools:
            for test_action in tool['tests']:
                url = '/api/v1/{}'.format(tool['uri'])
                data = {
                    'text':  urllib.parse.unquote(tool['tests'][test_action]['input']),
                    'action': test_action
                }
                print("running tests for {}\n{}".format(url, data))
                rv = self.app.post(url, data=data)
                self.assertIn(tool['tests'][test_action]['output'], rv.data.decode())

    def test_error_handling(self):
        """Test the API for each tool."""
        url = '/base64-encode-decode?text=abc&action=decode'
        rv = self.app.get(url)
        self.assertIn('Base64 Encoder/Decoder', rv.data.decode())
        self.assertIn('Encode/Decode base64 text.', rv.data.decode())
        self.assertIn('ERROR: Incorrect padding', rv.data.decode())
