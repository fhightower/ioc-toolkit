#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tools used in the ioc_toolkit."""

import base64
import html
import ipaddress
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


def html_escape(text, action):
    """Escape/Unescape html."""
    response = str()
    error = False

    if action == 'unescape':
        try:
            response = html.unescape(text)
        except Exception as e:
            error = True
            response = str(e)
    elif action == 'escape':
        try:
            response = html.escape(text)
        except Exception as e:
            error = True
            response = str(e)
    else:
        raise RuntimeError('Unknown action provided to html_escape function: {}'.format(action))

    return response, error


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
        raise RuntimeError("Unknown action provided to base64_encode_decode function: {}".format(action))

    return response, error


def ipv6_expand_compress(text, action):
    """Expand or collapse an IPv6 address."""
    response = str()
    error = False

    try:
        i = ipaddress.IPv6Address(text)
    except Exception as e:
        error = True
        response = str(e)
    else:
        if action == 'expand':
            try:
                response = i.exploded
            except Exception as e:
                error = True
                response = str(e)
        elif action == 'compress':
            try:
                response = i.compressed
            except Exception as e:
                error = True
                response = str(e)
        else:
            raise RuntimeError("Unknown action provided to ipv6_expand_compress function: {}".format(action))

    return response, error
