#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tools used in the ioc_toolkit."""

import base64
import html
import urllib.parse


def url_encode_decode(text, action):
    """Handle URL encoding/decoding."""
    response = str()
    error = False

    if action == 'decode':
        try:
            response = urllib.parse.unquote(text)
        except Exception as e:
            error = True
            response = str(e)
    elif action == 'encode':
        try:
            response = urllib.parse.quote(text)
        except Exception as e:
            error = True
            response = str(e)
    else:
        raise RuntimeError('Unknown action provided to url_encode_decode function: {}'.format(action))

    return response, error


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
    response = str()
    error = False

    if action == 'decode':
        try:
            response = text.encode('idna').decode('utf-8')
        except Exception as e:
            error = True
            response = str(e)
    elif action == 'encode':
        try:
            response = text.encode('utf-8').decode('idna')
        except Exception as e:
            error = True
            response = str(e)
    else:
        raise RuntimeError('Unknown action provided to punycode function: {}'.format(action))

    return response, error


def base64_encode_decode(text, action):
    """Handle base 64 encoding/decoding."""
    response = str()
    error = False

    if isinstance(text, str):
        text = text.encode('utf-8')

    if action == 'decode':
        try:
            response = base64.b64decode(text).decode('utf-8')
        except Exception as e:
            error = True
            response = str(e)
    elif action == 'encode':
        try:
            response = base64.b64encode(text).decode('utf-8')
        except Exception as e:
            error = True
            response = str(e)
    else:
        raise RuntimeError("Unknown action provided to url_encode_decode function: {}".format(action))

    return response, error
