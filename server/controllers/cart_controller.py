from flask import request, jsonify
from flask_login import current_user
from models import Cart, CartItem, Product

@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    product_id = request.json['product_id']
    quantity = request.json.get('quantity', 1)

    # Check if user is logged in
    if not current_user.is_authenticated:
        return jsonify({'error': 'User not logged in'}), 401

    # Find the product
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    # Check if the product is already in the cart
    cart_item = CartItem.query.filter_by(cart_id=current_user.cart.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart=current_user.cart, product=product, quantity=quantity)
        current_user.cart.items.append(cart_item)

    db.session.commit()
    return jsonify({'message': 'Product added to cart'})

@app.route('/cart/remove', methods=['DELETE'])
def remove_from_cart():
    product_id = request.json['product_id']

    # Check if user is logged in
    if not current_user.is_authenticated:
        return jsonify({'error': 'User not logged in'}), 401

    cart_item = CartItem.query.filter_by(cart_id=current_user.cart.id, product_id=product_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'message': 'Product removed from cart'})
    else:
        return jsonify({'error': 'Product not found in cart'}), 404

@app.route('/cart', methods=['GET'])
def get_cart_items():
    # Check if user is logged in
    if not current_user.is_authenticated:
        return jsonify({'error': 'User not logged in'}), 401

    cart_items = current_user.cart.items
    return jsonify([{'product_id': item.product_id, 'quantity': item.quantity} for item in cart_items])

@app.route('/cart/update', methods=['PUT'])
def update_cart_item_quantity():
    product_id = request.json['product_id']
    quantity = request.json['quantity']

    # Check if user is logged in
    if not current_user.is_authenticated:
        return jsonify({'error': 'User not logged in'}), 401

    cart_item = CartItem.query.filter_by(cart_id=current_user.cart.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity = quantity
        db.session.commit()
        return jsonify({'message': 'Cart item quantity updated'})
    else:
        return jsonify({'error': 'Product not found in cart'}), 404