#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from ioc_toolkit import ioc_toolkit


class IOCToolKitTestCase(unittest.TestCase):

    def setUp(self):
        self.app = ioc_toolkit.app.test_client()

    def _check_index(self, data):
        """Check that the index page is shown."""
        self.assertIn('Indicator of Compromise (IOC) Toolkit', data)
        assert 'Welcome to the Indicator of Compromise Toolkit!' in data

        for tool in ioc_toolkit.tools:
            self.assertIn(tool['name'], data)
            self.assertIn(tool['description'], data)

    def test_get_index(self):
        rv = self.app.get('/')
        self._check_index(rv.data.decode())

    def test_get_tool_pages(self):
        """Make sure the page for every tool is populating correctly."""
        for tool in ioc_toolkit.tools:
            rv = self.app.get('/{}'.format(tool['uri']))
            self.assertIn(tool['name'], rv.data.decode())
            self.assertIn(tool['description'], rv.data.decode())

    def test_non_exist_page(self):
        """Make sure requests to non-exist pages are redirected to the home page."""
        rv = self.app.get('/foobar')
        assert rv.status_code == 302

    def test_redirect_to_index(self):
        """Make sure requests to a non-existent page redirect to home page."""
        rv = self.app.get('/foobar', follow_redirects=True)
        assert rv.status_code == 200
        assert 'The page &#34;foobar&#34; does not exist. Try one of the links below.' in rv.data.decode()
        self._check_index(rv.data.decode())
