from flask import Flask,jsonify,request
import os
import json
import sys

def toJson(data):
    with open('vote.json','w',encoding='utf-8') as file:
        json.dump(data,file,ensure_ascii=False,indent='\t')

def loadJson():
    with open('vote.json','r',encoding='utf-8') as file:
        return json.load(file)

name = None
data = []
isVoted = []
toJson(data)
print("start")
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/vote', methods = ['POST'])
def vote():
    content = request.get_json()
    content = content['userRequest']    
    content = content['utterance']
    user = request.get_json()
    user = user['userRequest']['user']['id']
    global name,data,isVoted
    if content == u"투표하기":
         response_data = {
         "version" : "2.0",
            "template" : {
             "outputs" : [
                 {
                        "simpleText" : {
                         "text" : "후보자 이름을 적어주세요."
                            }
                        }
                    ]
                }
            }
    elif content == u"예":
        response_data = {
         "version" : "2.0",
            "template" : {
             "outputs" : [
                 {
                        "simpleText" : {
                         "text" : "투표에 참여해주셔서 감사합니다"
                            }
                        }
                    ]
                }
            }
        load = loadJson()
        print("load")
        for i in load :
            print("json파일 존재")
            if i["user"] == user :
                print("사용자 존재")
                response_data = {
                "version" : "2.0",
                    "template" : {
                    "outputs" : [
                        {
                                "simpleText" : {
                                "text" : "이미 투표하셨습니다."
                            }
                        }
                    ]
                }
            }
                isVoted.append(user)
        if user not in isVoted :
            print("사용자 비존재")
            data.append({"name":name, "user":user})
            toJson(data)
            print("데이터 저장")
    elif content == u"아니요":
        response_data = {
         "version" : "2.0",
            "template" : {
             "outputs" : [
                 {
                        "simpleText" : {
                         "text" : "투표에 참여해주십시오."
                            }
                        }
                    ]
                }
            }
    else:
        if len(content) != 3:
            response_data = {
         "version" : "2.0",
            "template" : {
             "outputs" : [
                 {
                        "simpleText" : {
                         "text" : "이름을 정확히 적어주세요."
                            }
                        }
                    ]
                }
            }
        else:
            name = content
            response_data ={
        "version": "2.0",
        "template": {
            "outputs": [
            {
                "simpleText": {
                "text": name + "님에게 투표하시겠습니까?"
                }
            }
            ],
            "quickReplies": [
         {
                "action": "message",
                "label": "예"
            },
          {
                "action": "message",
                "label": "아니요"
            }
        ]
        }
        }
    return jsonify(response_data)

if __name__ == "__main__" :
    app.run(host="0.0.0.0", port = "5000")

