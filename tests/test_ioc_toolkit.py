#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Run generic tests against the framework."""

import unittest

from ioc_toolkit import ioc_toolkit


class IOCToolkitUITestCase(unittest.TestCase):

    def setUp(self):
        self.app = ioc_toolkit.app.test_client()

    def _check_index(self, data):
        """Check that the index page is shown."""
        self.assertIn('Indicator of Compromise (IOC) Toolkit', data)
        assert 'Indicator of Compromise Toolkit' in data

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
            self.assertIn(tool['description'].split("<")[0], rv.data.decode())

    def test_missing_text(self):
        """Make sure a error message is shown for requests without text."""
        for tool in ioc_toolkit.tools:
            rv = self.app.get('/{}?action=Decode'.format(tool['uri']))
            self.assertIn(tool['name'], rv.data.decode())
            self.assertIn(tool['description'].split("<")[0], rv.data.decode())
            assert 'Please enter some text to decode' in rv.data.decode()

    def test_missing_action(self):
        """Make sure a error message is shown for requests without text."""
        for tool in ioc_toolkit.tools:
            rv = self.app.get('/{}?text=test'.format(tool['uri']))
            self.assertIn(tool['name'], rv.data.decode())
            self.assertIn(tool['description'].split("<")[0], rv.data.decode())

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


class IOCToolkitAPITestCase(unittest.TestCase):

    def setUp(self):
        self.app = ioc_toolkit.app.test_client()

    def test_api_docs(self):
        """Make sure all of the api pages return basic usage instructions."""
        for tool in ioc_toolkit.tools:
            rv = self.app.get('/api/v1/{}'.format(tool['uri']))
            assert 'Usage: ' in rv.data.decode()
            assert 'An example JSON body is:' in rv.data.decode()

    def test_empty_post(self):
        """Make sure all of the api pages return basic usage instructions if they receive an empty post request."""
        for tool in ioc_toolkit.tools:
            rv = self.app.post('/api/v1/{}'.format(tool['uri']))
            assert "Usage: " in rv.data.decode()

        for tool in ioc_toolkit.tools:
            rv = self.app.post('/api/v1/{}'.format(tool['uri']), data={})
            assert "Usage: " in rv.data.decode()


class IOCToolkitLegacyTests(unittest.TestCase):

    def setUp(self):
        self.app = ioc_toolkit.app.test_client()

    def test_punycode_decode(self):
        """Make sure the legacy, punycode coverter is working properly."""
        for tool in ioc_toolkit.tools:
            rv = self.app.post('/api/v1/convert?to=text&from=punycode'.format(tool['uri']), data='xn--l3h.com')
            assert '☁.com' in rv.data.decode()
