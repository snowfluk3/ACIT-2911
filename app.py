import json
import sys
from datetime import date
from pathlib import Path

import jsonschema
import requests
from datetime import timedelta

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

