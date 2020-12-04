import string

from flask import Flask, request, jsonify, Response,send_file
import json
import  random

app = Flask(__name__)


@app.route("/",methods=['GET'])
def test():

    return Response(response="helloworld",status=200)

@app.route("/getKeys",methods=['GET'])
def getKeys():

    json_request = request.get_json()
    if(json_request['op'] == 'GET_ONE'):
        pass
    elif(json_request['op'] == 'GET_ALL'):
        pass


