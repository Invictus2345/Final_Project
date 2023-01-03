from crypt import methods
from flask import Flask, render_template, request, session, redirect, flash
from flask_app import app
from flask_app.models.home_model import Home
from flask_app.models.user_model import User
from flask_app.models.inspection_model import Inspection
import requests

app = Flask(__name__)


@app.route('/create_inspection')
def create_inspection():
    return render_template('/inspection.html')

api_url = 'https://api.api-ninjas.com/v1/mortgagecalculator?loan_amount=200000&interest_rate=3.5&duration_years=30'
@app.route('/api')
def api_route():
    response = requests.get(api_url, headers={'X-Api-Key': 'YFZMY+8nGEBnzglhbKYvsZQ==BcGAhzQnYL31wttZ'})
    if response.status_code == requests.codes.ok:
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)