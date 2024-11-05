from flask import request, jsonify
from models import Product

@app.route('/products', methods=['POST'])
def create_product():
    # ...