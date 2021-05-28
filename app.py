#!/usr/bin/env python3
import os, sys
from flask import Flask, render_template, request
from flask.json import jsonify
from terms import get_term
from definitions import get_definitions

# create the app
if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    app = Flask(__name__, template_folder=template_folder)
else:
    app = Flask(__name__)

# get a static collection of all definitions
definitions = get_definitions()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    params = request.get_json()

    # get the name and term
    term = get_term(params['name'])
    name = f"{term} {params['name']}"

    # get the definition
    definition = definitions[term] if term in definitions else []

    # expose the result
    return { 'name': name, 'definition': definition }

app.run()
