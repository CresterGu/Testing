from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock data for testing
items = [
    {"id": 1, "name": "Item 1", "description": "This is the first item."},
    {"id": 2, "name": "Item 2", "description": "This is the second item."}
]

# Helper function to find an item by ID
def find_item(item_id):
    return next((item for item in items if item["id"] == item_id), None)

# Home route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the testing API!"})

# Get all items
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

# Get a single item by ID
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = find_item(item_id)
    if item:
        return jsonify(item)
    else:
        return jsonify({"error": "Item not found"}), 404

# Create a new item
@app.route('/items', methods=['POST'])
def create_item():
    new_item = request.json
    if not new_item.get("name") or not new_item.get("description"):
        return jsonify({"error": "Name and description are required"}), 400

    new_item["id"] = max(item["id"] for item in items) + 1 if items else 1
    items.append(new_item)
    return jsonify(new_item), 201

# Update an existing item
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.json
    item.update({
        "name": data.get("name", item["name"]),
        "description": data.get("description", item["description"])
    })
    return jsonify(item)

# Delete an item
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    items.remove(item)
    return jsonify({"message": "Item deleted"})

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=8000)
