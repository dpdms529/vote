from flask import Flask,jsonify,request
import os
import json
import sys

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/vote', methods = ['POST'])
def wait():
    content = request.get_json()
    content = content['userRequest']['utterance']

    response_data = {
         "version" : "2.0",
            "template" : {
             "outputs" : [
                 {
                        "simpleText" : {
                         "text" : "투표 시간이 아닙니다."
                            }
                        }
                    ]
                }
            } 
    return jsonify(response_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = "5000")