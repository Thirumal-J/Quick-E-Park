from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/',)
def index():
    return "Hello!! This is geolocation location api"

@app.route('/saveloc',methods=['POST'])
def saveloc():
 rf=request.form
 for key in rf.keys():
  data=key
 print(data)
 data_dic=json.loads(data)
 print(data_dic.keys())
 lat=data_dic['loc'][0]
 lon=data_dic['loc'][1]
 resp_dic={"lat":lat,"lon":lon}
 resp = jsonify(resp_dic)
 resp.headers['Access-Control-Allow-Origin']='*'
 return resp




if(__name__=="__main__"):
    #app.run(host='192.168.0.7')
    app.run(port=5003, debug=True)