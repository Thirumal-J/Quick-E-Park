from flask import Flask, jsonify
import constants as const

response = {"status_code": "", "status_msg": "", "status_type":"", "data":""}

def createJSONResponse(outputJson, status_code= const.DEFAULT,status_msg=const.DEFAULT, status_type=const.DEFAULT):
    response["status_code"] = status_code
    response["status_msg"] =  status_msg
    response["status_type"] = status_type
    response["data"] = outputJson
    return jsonify(response)