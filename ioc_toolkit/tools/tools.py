#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tools used in the ioc_toolkit."""

import html
import urllib.parse


def url_encode_decode(text, action):
    """Handle URL encoding/decoding."""
    if action == 'decode':
        return urllib.parse.unquote(text)
    elif action == 'encode':
        return urllib.parse.quote(text)
    else:
        raise RuntimeError('Unknown action provided to url_encode_decode function: {}'.format(action))


# def html_escape(text, action):
#     """Handle URL encoding/decoding."""
#     if action == 'decode':
#         return html.unescape(text)
#     elif action == 'encode':
#         return html.escape(text)
#     else:
#         raise RuntimeError("Unknown action provided to url_encode_decode function: {}".format(action))


def punycode(text, action):
    """Convert punycode to unicode and visa-versa."""
    if action == 'decode':
        return text.encode('idna').decode('utf-8')
    elif action == 'encode':
        return text.encode('utf-8').decode('idna')
    else:
        return RuntimeError('Unknown action provided to punycode function: {}'.format(action))
