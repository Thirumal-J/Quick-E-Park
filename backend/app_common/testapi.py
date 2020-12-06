from flask import Flask, jsonify
import common
import constants
app = Flask(__name__)

@app.route('/getResponse', methods=['GET'])
def getResponse():
    # in your own APIs, Kindly use the below method and send your own Response Objects
    data = [{'name':'thiru','age':'36'},{'name':'sheharaz','age':'23'}]
    
    print(data[0])
    return common.createJSONResponse(data, constants.SUCCESS_CODE, constants.EMAIL_SUCCESS_MSG+"xxx@gmail.com", constants.SUCCESS)

if __name__ == '__main__':
    app.run(debug=True)