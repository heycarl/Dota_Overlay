from flask import Flask, request
import json
import variables

app = Flask(__name__)


@app.route('/', methods=['POST'])
def result():
    json.dump(request.json, open("data/response.json", 'w'), sort_keys=True, indent=4)
    return 'Received !'  # response to your request.


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)
