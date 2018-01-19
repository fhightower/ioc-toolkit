#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import flash, Flask, render_template, redirect, request, url_for

app = Flask(__name__)
app.secret_key = 'abc'

tools = [{
    'name': 'Punycode',
    'description': 'Convert punycode to unicode and visa-versa',
    'function': 'punycode'
}]


@app.route("/")
def index():
    return render_template("index.html", tools=tools)


@app.route("/punycode")
def punycode():
    description = None

    for tool in tools:
        if tool['function'] == 'punycode':
            description = tool['description']
            break

    return render_template("punycode.html", description=description)


@app.route("/api/v1/convert", methods=['POST'])
def api():
    domain = request.form.get('domain')

    if domain is None:
        domain = request.data.decode("utf-8")

        if domain is None:
            return "Please enter a domain"

    if (request.args['to'] == 'unicode' or request.args['to'] == 'text') and (request.args['from'] == 'punycode' or request.args['from'] == 'idna'):
        return domain.encode("utf-8").decode("idna")


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
