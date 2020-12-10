from flask import Flask, jsonify
import constants as const

response = {"status_code": "", "status_msg": "", "status_type":"", "data":""}

def createJSONResponse(outputJson, status_code= const.SUCCESS_CODE,status_msg=const.DEFAULT_SUCCESS_MSG, status_type=const.Status_type[0]):
    response["status_code"] = status_code
    response["status_msg"] =  status_msg
    response["status_type"] = status_type
    response["data"] = outputJson
    return jsonify(response)

