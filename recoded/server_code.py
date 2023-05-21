from flask import Flask, request, jsonify

app = Flask(__name__)

number = None  # initialize the number to None
end = False
state = 1
get_graph  = 0

@app.route('/', methods=['GET'])
def home():
    return 'Hello, world!'

@app.route('/store_number', methods=['POST'])
def store_number():
    global number
    data = request.get_json()
    number = data['number']
    return jsonify({'message': 'Number stored successfully.'})

@app.route('/get_number', methods=['GET'])
def get_number():
    global number
    x = number 
    number = -1
    return jsonify({'number': x})

@app.route('/state', methods=['POST','GET'])
def get_state():
    global state
    if (request.method=='POST'):
        data = request.get_json()
        state = data['state']
        return jsonify({'message': 'Number stored successfully.'})
    elif (request.method=='GET'):
        return jsonify({'state': state})
    return jsonify({'message': 'Wrong request method type'})

@app.route('/end', methods=['POST','GET'])
def set_end():
    global end
    if (request.method=='POST'):
        data = request.get_json()
        end = data['end']
        return jsonify({'message': 'Number stored successfully.'})
    elif (request.method=='GET'):
        return jsonify({'end': end})
    return jsonify({'message': 'Wrong request method type'})

@app.route('/get_graph', methods=['POST','GET'])
def set_graph():
    global get_graph
    if (request.method=='POST'):
        data = request.get_json()
        get_graph = data['get_graph']
        return jsonify({'message': 'Number stored successfully.'})
    elif (request.method=='GET'):
        x = get_graph
        get_graph = 0
        return jsonify({'get_graph': x})
    return jsonify({'message': 'Wrong request method type'})

if __name__ == '__main__':
    app.run()  # start the Flask app