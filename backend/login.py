from flask import Flask,make_response,request,jsonify
import psycopg2
import json
import jwt
import datetime
from functools import wraps

app=Flask(__name__)

app.config['SECRET_KEY']='secret'


def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token=None
        if 'token' in request.headers:
            token=request.headers['token']
        #token=request.args.get('token')
        if not token:
            return jsonify({'message':'Token missing'}),403
        try:
            data=jwt.decode(token,app.config['SECRET_KEY'])
        except:
            return jsonify({'message':'token is invalid'}),403
        return f(*args,**kwargs)
    return decorated

DB_HOST="192.168.99.100"
DB_NAME="QuickEPark"
DB_USER="postgres"
DB_PASS="Pass@123"

User_table="Users"
# conn =psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST)
# cur=conn.cursor()
# #cur.execute("CREATE TABLE Users (ID INT, Username varchar, PasswordHash varchar);")
# cur.execute("INSERT INTO USERS VALUES (1,'SHEHARAZ','PASSWORD');")
# conn.commit()
# conn.close()

@app.route("/")
@token_required
def index():
    return "Hello!! This is login authentication api"

@app.route("/test")
def authe():
    auth=request.authorization

    if auth and auth.password=='password':
        token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=15)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})
    return make_response('Could not verify',401,{'WWW-Authenticate': 'Basic realm="Login Required"'})

@app.route("/loginvalid",methods=['POST'])
#@token_required
def loginvalid():
    result=-1
    try:
        conn =psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST)
        cur=conn.cursor()
        Username=""
        Password=""
        try:
            Username=request.json["User"]["Username"]
            Password=request.json["User"]["Password"]
        except:
            print("Exception input user and password format")

        SQL="select 1 from "+ User_table +" where Username in ('"+ Username +"') and PasswordHash in ('"+Password+"')"
        try:
            cur.execute(SQL)
            result=cur.fetchall()
        except:
            print(SQL)
            print("Table doesn't exist or null values found")
        if result==[]:
            result="No user found"
        else:
            result=result[0][0]
        conn.commit()
        conn.close()
    except:
        print("Invalid database")
    return str(result)

if __name__=="__main__":
    app.run(port=5000,debug=True)