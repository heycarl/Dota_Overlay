from flask import Flask, request
import json

app = Flask(__name__)


@app.route('/', methods=['POST'])
def result():
    json.dump(request.json, open("data/response.json", 'w'), sort_keys=True, indent=4)
    return 'Received !'  # response to your request.


app.run(host='127.0.0.1', port=3000)
