#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from flask import flash, Flask, Blueprint, render_template, redirect, request, url_for

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "./")))
from tools.tools import url_encode_decode, punycode

app = Flask(__name__)
app.secret_key = 'abc'

tools = [{
    'name': 'Punycode',
    'description': 'Convert punycode to unicode and visa-versa',
    'function': punycode,
    'actions': ['decode', 'encode'],
    'uri': 'punycode'
}, {
    'name': 'URL Encoder/Decoder',
    'description': 'Encode/Decode a url',
    'function': url_encode_decode,
    'actions': ['encode', 'decode'],
    'uri': 'url-encode-decode',
}]


def _get_route_data(route_name):
    """Return data about the route with the given name."""
    route_found = False

    for tool in tools:
        if tool['uri'] == route_name:
            name = tool['name']
            description = tool['description']
            function = tool['function']
            actions = tool['actions']

            route_found = True
            break

    if route_found:
        return name, description, function, actions
    else:
        return None, None, None, None


ioc_toolkit_blueprint = Blueprint('ioc_toolkit_blueprint', __name__, template_folder='templates')


@ioc_toolkit_blueprint.route('/<page>')
def simple_form(page):
    template = "simple-form.html"
    name, description, function, actions = _get_route_data(page)

    if name is None:
        flash('The page "{}" does not exist. Try one of the links below.'.format(page), 'error')
        return redirect(url_for('index'))

    action = None

    if request.args.get('action'):
        action = request.args['action'].lower()

    if action == 'clear':
        request.args = []
        return render_template(template, name=name, description=description, function=function, actions=actions, uri=page)

    if request.args.get('text') and action:
        response = function(request.args.get('text'), action)

        return render_template(template, name=name, description=description, function=function, actions=actions, uri=page, output=response, text=request.args.get('text'))
    elif action:
        flash('Please enter some text to {}.'.format(action), 'error')
        return render_template(template, name=name, description=description, function=function, actions=actions, uri=page)
    else:
        return render_template(template, name=name, description=description, function=function, actions=actions, uri=page)


@ioc_toolkit_blueprint.route('/api/v1/<page>', methods=['GET', 'POST'])
def simple_api(page):
    name, description, function, actions = _get_route_data(page)

    usage = 'Usage: To use this branch, make a POST request to /api/v1/{} with a JSON body that includes a "text" key providing the text which will be operated on and an "action" which will tell the API what to do with the text. The available action(s) for this page is/are: {}.'.format(page, ", ".join(actions))

    if name is None:
        return 'The requested page ({}) does not exist.'.format(page)
    else:
        if request.method == 'POST':
            # TODO: also check request.data
            if not request.form.get('action') or not request.form.get('text'):
                return 'Usage: To use this branch, make a POST request to /api/v1/{} with a JSON body that includes a "text" key providing the text which will be operated on and an "action" which will tell the API what to do with the text. The available action(s) for this page is/are: {}.'.format(page, ", ".join(actions))
            else:
                return function(request.form.get('text'), request.form.get('action'))
        else:
            return usage


app.register_blueprint(ioc_toolkit_blueprint)


@app.route("/")
def index():
    return render_template("index.html", name='Indicator of Compromise Toolkit', description='Indicator of Compromise (IOC) Toolkit in progress. Check back soon for a list of available tools.', tools=tools)


"""LEGACY CODE THAT SHOULD BE KEPT FOR THE TIME BEING:"""
@app.route("/api/v1/convert", methods=['POST'])
def api():
    """Keep this code for legacy purposes."""
    domain = request.form.get('domain')

    if domain is None:
        domain = request.data.decode("utf-8")

        if domain is None:
            return "Please enter a domain"

    if (request.args['to'] == 'unicode' or request.args['to'] == 'text') and (request.args['from'] == 'punycode' or request.args['from'] == 'idna'):
        return domain.encode("utf-8").decode("idna")


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
