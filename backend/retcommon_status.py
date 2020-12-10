import json
from flask import jsonify

response = {"status_code": "-1", "status_msg": "", "status_desc":"Recheck return json status method call", "status_type":"", "data":""}

def createJSONResponse(status="default", status_who="NoWho", data="No Data Passed"):
    with open('process_status.JSON') as f:
      data_json = json.load(f)
    
    dict_status=data_json[status.lower()]
    if status!="default" and status_who!="NoWho":
      response["status_code"] = dict_status["status"][status_who.lower()]["status_code"]
      response["status_desc"]=  dict_status["status"][status_who]["status_desc"]
    response["status_msg"] =  dict_status["status_message"]
    response["status_type"] = dict_status["status_type"]
    response["data"] = data
    return jsonify(response)
        

#print(data["success"])
#print(retconstjson("success", "Generic"))