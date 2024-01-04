from flask import Flask, jsonify, url_for, render_template
from algotrade import AlgoTrade


app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/signal/<ticker>', methods=['GET'])
def get_signal(ticker):
    algo = AlgoTrade(ticker)
    

    return jsonify(algo.getJSON())

if __name__ == '__main__':
    app.run(debug=True)