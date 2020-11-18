from flask import Flask,jsonify,request
import os
import json
import sys

position = input("position : ")
filename = position + ".json"
def toJson(data):
    with open(filename,'w',encoding='utf-8') as file:
        json.dump(data,file,ensure_ascii=False,indent='\t')

def loadJson():
    with open(filename,'r',encoding='utf-8') as file:
        return json.load(file)

candidate = []
c = None
while c != "ㄴ":
    c = input("후보자 등록 : ")
    if c!="ㄴ":
        candidate.append(c)
candidate.append("기권")
name = []
data = []
for i in candidate:
    data.append({"name":i,"count":0})
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
                         "text" : "후보자 이름을 적어주세요.\n※ 기권하시려면 기권이라고 적어주세요."
                            }
                        }
                    ]
                }
            }
    elif content == u"후보자":
        text = ""
        for i in candidate:
            text = text + i + '\n'
        text = text[:-1]
        response_data = {
         "version" : "2.0",
            "template" : {
             "outputs" : [
                 {
                        "simpleText" : {
                         "text" : text
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

        if user in isVoted:
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
        else:
            print("사용자 비존재")
            for i in data:
                for j in name:
                    if j["user"] ==  user:
                        print(user + "데이터 찾음")
                        if i["name"] == j["name"]:
                            print(user + "가 투표한 후보자 찾음")
                            i["count"] = i["count"] + 1
                            toJson(data)
                            print("데이터 저장")
                            isVoted.append(user)

    elif content == u"아니요":
        response_data = {
         "version" : "2.0",
            "template" : {
             "outputs" : [
                 {
                        "simpleText" : {
                         "text" : "투표에 참여해주세요."
                            }
                        }
                    ]
                }
            }
    else:
        if content not in candidate:
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
            for i in name:
                if i["user"] ==user:
                    print("name데이터 삭제")
                    name.remove(i)
            name.append({"name":content,"user":user})
            who = content
            if who=="기권":
                response_data ={
        "version": "2.0",
        "template": {
            "outputs": [
            {
                "simpleText": {
                "text": "기권하시겠습니까?"
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
            else:
                response_data ={
        "version": "2.0",
        "template": {
            "outputs": [
            {
                "simpleText": {
                "text": who + "님에게 투표하시겠습니까?"
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
            print(name)
    return jsonify(response_data)

if __name__ == "__main__" :
    app.run(host="0.0.0.0", port = "5000")


