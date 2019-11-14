# -*- coding: utf-8 -*-
from flask import Response, json, session, Flask, render_template, jsonify, request, redirect, url_for
import json, datetime, os

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/')
def home():
    return(jsonify('success'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
