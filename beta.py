from flask import Flask, request
import json
from threading import Thread
import time

app = Flask(__name__)


def flex():
    @app.route('/', methods=['POST'])
    def result():
        json.dump(request.json, open("data/response.json", 'w'), sort_keys=True, indent=4)
        return 'Received !'  # response to your request.
    app.run(host='127.0.0.1', port=3000)


def flex2():
    while 1:
        print("flex")
        time.sleep(1)


thread1 = Thread(target=flex)
thread2 = Thread(target=flex2)
thread1.start()
thread2.start()
thread1.join()
thread2.join()
