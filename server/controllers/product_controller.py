import json

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)

@app.route('/products')
def get_products():
    with open('static/products.json', 'r') as f:
        products = json.load(f)
    return jsonify(products)