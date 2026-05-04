import json
import sys
from datetime import date
from pathlib import Path

import jsonschema
import requests
from datetime import timedelta

from flask import Flask, jsonify, render_template, request

from model import db, init_db

app = Flask(__name__)

@app.before_request
def open_db():
    db.connect(reuse_if_open=True)

@app.teardown_request
def close_db(exc):
    if not db.is_closed():
        db.close()

init_db()

