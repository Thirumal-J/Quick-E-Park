#exception message printing pending
from flask import Flask,make_response,request,jsonify
import psycopg2
import json
import jwt
import datetime
from functools import wraps
import statuswho
import retcommon_status

app=Flask(__name__)

app.config['SECRET_KEY']='secret'

User_table="tbl_user"
parking_table="tbl_parkdetails"
activepark_view="uv_getparkdetails"

DB_HOST="192.168.99.100"
DB_NAME="ARPB"
DB_USER="postgres"
DB_PASS="Password"

@app.route("/")
def index():
    return "Hello!! This is buy ticket api"

@app.route("/viewticket",methods=['POST'])
def viewticket():
    result=-1
    jsonresult={}
    status="default"
    email=""
    status_who=""
    parkdate=""
    timeremaining=""
    parkinglocation=""
    parkingfare=""
    parkedcarregno=""
    # carregno=""
    # minutesparking=""
    # parkloc=""
    uid_temp=""
    uid=""
    try:
        email=request.json["Email"]
        status="success"
    except:
        status="error"
        status_who=statuswho.JSON_INPUT_INCORRECT
    try:
        conn =psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST)
        cur=conn.cursor()
    except:
        status="error"
        status_who=statuswho.DB_CONNECTION_FAILED
    if status=="success":
        try:
            SQL="select uid from "+ User_table +" where email in ('"+ email +"')"
            cur.execute(SQL)
            uid_temp=cur.fetchall()
            if uid_temp==[]:
                result="No user found"
                status="error"
                status_who=statuswho.LOGIN_STATUS_FAIL
            else:
                try:
                    uid=str(uid_temp[0][0])
                    SQL="select 1 from "+ activepark_view + " where uid in ('" + uid + "')"
                    cur.execute(SQL)
                    result=cur.fetchall()
                    if result==[]:
                        status="error"
                        status_who=statuswho.NO_DATA_TO_DISPLAY
                    else:
                        try:
                            SQL="select parkingstartdate,timeremaining,parkinglocation,parkingfare,parkedcarregno from " + activepark_view + " where uid in ('" + uid + "')"
                            cur.execute(SQL)
                            result=cur.fetchall()
                            parkdate=str(result[0][0])
                            timeremaining=str(result[0][1])
                            parkinglocation=str(result[0][2])
                            parkingfare=str(result[0][3])
                            parkedcarregno=str(result[0][4])
                            # jsonresult='{"parkdate":"'+parkdate+'","timeremaining":"'+ timeremaining+'", "parkinglocation:"'+parkinglocation+'", "parkingfare:"'+parkingfare+'", "parkedcarregno""'+parkedcarregno +'"}'
                            jsonresult={"parkdate":parkdate,"timeremaining":timeremaining, "parkinglocation":parkinglocation, "parkingfare":parkingfare, "parkedcarregno":parkedcarregno}
                            status="success"
                            status_who=statuswho.GENERIC_STATUS
                        except:
                            status_who=statuswho.TABLE_DOESNOT_EXIST
                            status="error"
                except:
                    status="error"
                    status_who=statuswho.TABLE_DOESNOT_EXIST
            conn.commit()
            conn.close()
        except:
            status="error"
            status_who=statuswho.TABLE_DOESNOT_EXIST
    if result==[]:
            result=-1
    return retcommon_status.createJSONResponse(status,status_who,jsonresult)

@app.route("/buyticket",methods=['POST'])
#@token_required
def buyticket():
    result=-1
    status="default"
    email=""
    carregno=""
    minutesparking=""
    parkloc=""
    uid_temp=""
    uid=""
    try:
        email=request.json["Email"]
        carregno=request.json["Parkedcarregno"]
        minutesparking=request.json["Minutesparking"]
        parkloc=request.json["Parkingloc"] 
        status="success"
    except:
        status="error"
        status_who=statuswho.JSON_INPUT_INCORRECT
    try:
        conn =psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST)
        cur=conn.cursor()
    except:
        status="error"
        status_who=statuswho.DB_CONNECTION_FAILED
    if status=="success":
        try:
            SQL="select uid from "+ User_table +" where email in ('"+ email +"')"
            cur.execute(SQL)
            uid_temp=cur.fetchall()
            if uid_temp==[]:
                result="No user found"
                status="error"
                status_who=statuswho.LOGIN_STATUS_FAIL
            else:
                try:
                    uid=str(uid_temp[0][0])
                    SQL="select 1 from "+ parking_table + " where uid in ('" + uid + "')"
                    #SQL="select 1 from " + parking_table + " where uid in ('"+ uid + "')"# and ParkedCarRegNo in ('"+ carregno +"') and parkingactive in ('1')"
                    print(SQL)
                    cur.execute(SQL)
                    result=cur.fetchall()
                    if result==[]:
                        try:
                            SQL="insert into " + parking_table + " values( " + uid + " , '1',  now(), now() + interval '1' minute * "+ minutesparking + ",'"+ parkloc +"',0,'" + carregno+"')"
                            print(SQL)
                            cur.execute(SQL)
                            status="success"
                            status_who=statuswho.PARKING_SUCCESSFUL
                        except:
                            status_who=statuswho.PARKING_INSERTION_FAILED
                            status="error"
                    else:
                        status="error"
                        status_who=statuswho.PARKING_ALREADY_EXISTS
                except:
                    status="error"
                    status_who=statuswho.TABLE_DOESNOT_EXIST
            conn.commit()
            conn.close()
        except:
            status="error"
            status_who=statuswho.TABLE_DOESNOT_EXIST
    if result==[]:
            result=-1
    return retcommon_status.createJSONResponse(status,status_who)

if __name__=="__main__":
    app.run(port=5004,debug=True)