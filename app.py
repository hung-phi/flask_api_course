from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [
    {
        'name': 'Mystore',
        'items': [
            {
                'name': 'Sunglasses',
                'price': 1.99,
            }
        ]
    }
]

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)

@app.route('/store', methods=['GET'])
def get_all_store():
    return jsonify({'stores': stores})

@app.route('/store/<string:name>', methods=['GET'])
def get_store(name):
    return jsonify([store for store in stores if store['name'] == name])

@app.route('/store/<string:name>/item', methods=['POST', 'GET'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'store not found'})


def get_item_in_store(name):
    pass

app.run(port=5000, debug=True)