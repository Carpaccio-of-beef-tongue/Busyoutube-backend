from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    hello_api = {
        'greeting': "Hello World!"
    }
    return jsonify(hello_api)

if __name__ == '__main__':
    app.run(debug=True)
