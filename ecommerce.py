from flask import Flask, jsonify, request

app = Flask(__name__)

# Base de données simulée
products = []

# Route : Obtenir tous les produits
@app.route('/products', methods=['GET'])
def get_products():
    category = request.args.get('category')
    in_stock = request.args.get('inStock')
    filtered_products = products
    if category:
        filtered_products = [p for p in products if p['category'] == category]
    if in_stock:
        filtered_products = [p for p in filtered_products if p['stock'] > 0]
    return jsonify(filtered_products)

# Route : Ajouter un produit
@app.route('/products', methods=['POST'])
def add_product():
    product = request.json
    product['id'] = len(products) + 1
    products.append(product)
    return jsonify(product), 201

# Route : Obtenir un produit par ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product)

# Route : Mettre à jour un produit
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    data = request.json
    product.update(data)
    return jsonify(product)

# Route : Supprimer un produit
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global products
    products = [p for p in products if p['id'] != product_id]
    return jsonify({'message': 'Product deleted'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)
