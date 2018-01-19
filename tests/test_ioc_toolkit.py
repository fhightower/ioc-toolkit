#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from ioc_toolkit import ioc_toolkit


class IOCToolKitTestCase(unittest.TestCase):

    def setUp(self):
        self.app = ioc_toolkit.app.test_client()

    def test_get_index(self):
        rv = self.app.get('/')
        self.assertIn('Indicator of Compromise (IOC) Toolkit', rv.data.decode())

        for tool in ioc_toolkit.tools:
            self.assertIn(tool['name'], rv.data.decode())
            self.assertIn(tool['description'], rv.data.decode())

    def test_get_tool_pages(self):
        """Make sure the page for every tool is populating correctly."""
        for tool in ioc_toolkit.tools:
            rv = self.app.get('/{}'.format(tool['function']))
            self.assertIn(tool['name'], rv.data.decode())
            self.assertIn(tool['description'], rv.data.decode())
