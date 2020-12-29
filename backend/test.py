#exception message printing pending
from flask import Flask,make_response,request,jsonify
import psycopg2
import json
import jwt
import datetime
from functools import wraps
import statuswho
import retcommon_status
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import parking_fare
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

app.config['SECRET_KEY']='secret'

User_table="tbl_user"
parking_table="tbl_parkdetails"
activepark_view="uv_getparkdetails"
penalty_table="tbl_penalty"

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


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

DB_HOST="localhost"
DB_NAME="postgres"
DB_USER="postgres"
DB_PASS="Password"

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
def loginvalid():
    result=-1
    status="default"
    status_who=""
    Username=""
    Password=""
    authentication=""
    firstname=""
    surname=""
    email=""
    licenseNumber=""
    mobileNumber=""
    jsonresult={}
    #jsonstr=json.loads(request.json,strict=False)
    #print(jsonstr)
    try:
        Username=request.json["email"]
        Password=request.json["password"]
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
            SQL="select 1 from "+ User_table +" where email in ('"+ Username +"') and Password in ('"+Password+"')"
            cur.execute(SQL)
            result=cur.fetchall()
            if result==[]:
                result="false"
                status="error"
                status_who=statuswho.LOGIN_STATUS_FAIL
            else:
                try:
                    status="success"
                    status_who=statuswho.LOGIN_STATUS
                    authentication="true"
                    SQL="select name,surname,email,licenseno,mobileno from "+ User_table +" where email in ('"+ Username +"')"
                    cur.execute(SQL)
                    result=cur.fetchall()
                    firstname=str(result[0][0])
                    surname=str(result[0][1])
                    email=str(result[0][2])
                    licenseNumber=str(result[0][3])
                    mobileNumber=str(result[0][4])
                    jsonresult={"authentication": authentication,"email": email,"firstName": firstname,"lastName":surname,"licenseNumber": licenseNumber,"mobileNumber": mobileNumber}
                except:
                    status_who=statuswho.TABLE_DOESNOT_EXIST
                    status="error"
            conn.commit()
            conn.close()
        except:
            #print(SQL)
            status="error"
            status_who=statuswho.TABLE_DOESNOT_EXIST
    if result==[]:
            result=-1
    return retcommon_status.createJSONResponse(status,status_who,jsonresult)

@app.route("/viewticket",methods=['POST'])
def viewticket():
    result=-1
    # jsonresult={}
    jsonresult=[]
    status="default"
    email=""
    status_who=""
    parkdate=""
    timeremaining=""
    parkinglocation=""
    parkingfare=""
    parkedcarregno=""
    parkingEmail=""
    # carregno=""
    # minutesparking=""
    # parkloc=""
    uid_temp=""
    uid=""
    try:
        email=request.json["email"]
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
                            SQL="select parkingstartdate,timeremaining,parkinglocation,parkingfare,parkedcarregno,parkingEmail from " + activepark_view + " where uid in ('" + uid + "')"
                            cur.execute(SQL)
                            result=cur.fetchall()
                            for i in range(len(result)):
                                parkdate=str(result[i][0])
                                timeremaining=str(result[i][1])
                                parkinglocation=str(result[i][2])
                                parkingfare=str(result[i][3])
                                parkedcarregno=str(result[i][4])
                                parkingEmail=str(result[i][5]) 
                                # if(len(jsonresult) is None):                               
                                #     jsonresult={"parkingStartDate":parkdate,"remainingParkingDuration":timeremaining, "parkingLocation":parkinglocation, "parkingFare":parkingfare, "parkedCarRegNo":parkedcarregno,"parkingEmail":parkingEmail}
                                # else:
                                #     jsonresult=jsonresult+{"parkingStartDate":parkdate,"remainingParkingDuration":timeremaining, "parkingLocation":parkinglocation, "parkingFare":parkingfare, "parkedCarRegNo":parkedcarregno,"parkingEmail":parkingEmail}
                                jsonresult.append({"parkingStartDate":parkdate,"remainingParkingDuration":timeremaining, "parkingLocation":parkinglocation, "parkingFare":parkingfare, "parkedCarRegNo":parkedcarregno,"parkingEmail":parkingEmail})
                            # jsonresult='{"parkdate":"'+parkdate+'","timeremaining":"'+ timeremaining+'", "parkinglocation:"'+parkinglocation+'", "parkingfare:"'+parkingfare+'", "parkedcarregno""'+parkedcarregno +'"}'
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
    parkingfare=""
    jsonresult={}
    parkingEmail=""
    try:
        email=request.json["email"]
        carregno=request.json["parkedCarRegNo"]
        minutesparking=request.json["parkingDuration"]
        parkloc=request.json["parkedLocation"] 
        if(request.json["parkingEmail"]):
            parkingEmail=request.json["parkingEmail"]
        else:
            parkingEmail=email
        status="success"
        parkingfare=float(parking_fare.calfare(minutesparking))
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
                    SQL="select 1 from "+ parking_table + " where uid in ('" + uid + "') and parkedcarregno in ('" + carregno + "')"
                    #SQL="select 1 from " + parking_table + " where uid in ('"+ uid + "')"# and ParkedCarRegNo in ('"+ carregno +"') and parkingactive in ('1')"
                    print(SQL)
                    cur.execute(SQL)
                    result=cur.fetchall()
                    if result==[]:
                        try:
                            SQL="insert into " + parking_table + " values( " + uid + " , '1',  now(), now() + interval '1' minute * "+ minutesparking + ",'"+ parkloc +"','"+str(parkingfare)+"','" + carregno+"','" + parkingEmail+"')"
                            print(SQL)
                            cur.execute(SQL)
                            status="success"
                            status_who=statuswho.PARKING_SUCCESSFUL
                            jsonresult={"parkingFare":parkingfare}
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
    return retcommon_status.createJSONResponse(status,status_who,jsonresult)

def createpassword_new():
    result=-1
    status="default"
    status_who=""
    try:
        Username=request.json["email"]
        Password=request.json["password"]
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
        SQL_checkuser="select 1 from "+ User_table +" where Username in ('"+ Username +"')"
        cur.execute(SQL_checkuser)

        if(cur.fetchall()[0][0]==1):
            try:
                SQL="update "+ User_table +" set Password='"+ Password +"' where email='"+Username+"'"
                cur.execute(SQL)
                #result=cur.fetchall()
                status="success"
                status_who=statuswho.INSERTION_PASSWORD_SUCCESS
            except:
                status="error"
                status_who=statuswho.TABLE_DOESNOT_EXIST
        else:
            status="error"
            status_who=statuswho.INSERTION_PASSWORD_FAIL
        conn.commit()
        conn.close()
    return retcommon_status.createJSONResponse(status,status_who)


@app.route("/resetpassword",methods=['POST'])
def resetpassword():
    result=-1
    status="default"
    status_who=""
    try:
        Username=request.json["email"]
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
            SQL="select email from "+ User_table +" where email in ('"+ Username +"')"
            cur.execute(SQL)
            result=cur.fetchall()
        except:
            status="error"
            status_who=statuswho.TABLE_DOESNOT_EXIST
        if result==[]:
            result=0
            status="error"
            status_who=statuswho.LOGIN_STATUS_FAIL
        else:
            result=result[0][0]
            email_flag=SendEmail(result)
            if email_flag==0:
                status="success"
                status_who=statuswho.EMAIL_STATUS_SUCCESS
            else:
                status="error"
                status_who=statuswho.EMAIL_STATUS_FAILED
        conn.commit()
        conn.close()
        
    if result==[]:
        result=-1
    return retcommon_status.createJSONResponse(status,status_who,str(result))

def SendEmail(EmailId):
    try:
        html_string=""
        with open('EmailTemplate.html', 'r') as f: 
            html_string = f.read()
        #mail_content = 'Body'
        mail_content=html_string
        sender_address = 'mmicroservice@gmail.com'
        sender_pass = 'mmicroservice@123'
        receiver_address = EmailId
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Reset Password - Quick E Park' 
        message.attach(MIMEText(mail_content, 'html'))
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(sender_address, sender_pass)
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        flag=0
    except Exception as e:
        flag="1"
        print(e)
    return flag

@app.route("/viewfine",methods=['POST'])
def viewfine():
    result=-1
    parkingfine=""
    finedate=""
    jsonresult={}
    try:
        email=request.json["email"]
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
                    SQL="select 1 from "+ penalty_table + " where uid in ('" + uid + "')"
                    cur.execute(SQL)
                    result=cur.fetchall()
                    if result==[]:
                        status="error"
                        status_who=statuswho.NO_DATA_TO_DISPLAY
                    else:
                        try:
                            SQL="select parkingfine,finedate from " + penalty_table + " where uid in ('" + uid + "')"
                            cur.execute(SQL)
                            result=cur.fetchall()
                            parkingfine=str(result[0][0])
                            finedate=str(result[0][1])
                            # jsonresult='{"parkdate":"'+parkdate+'","timeremaining":"'+ timeremaining+'", "parkinglocation:"'+parkinglocation+'", "parkingfare:"'+parkingfare+'", "parkedcarregno""'+parkedcarregno +'"}'
                            jsonresult={"parkingfine":parkingfine,"finedate":finedate}
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

@app.route("/extendTicket",methods=['POST'])
def extendticket():
    result=-1
    status="default"
    status_who=""
    email=""
    carregno=""
    minutesextended=""
    parkloc=""
    uid_temp=""
    uid=""
    parkingfare=""
    parkingemail=""
    parkingStartDate=""
    parkingEndDate=""
    parkingfare_new=""
    jsonresult={}
    try:
        email=request.json["email"]
        carregno=request.json["parkedCarRegNo"]
        # parkStartDate=request.json["parking"]
        minutesextended=request.json["timeToExtend"]
        # parkloc=request.json["parkedLocation"]
        parkingemail=request.json["parkingEmail"]
        status="success"
        #parkingfare=float(parking_fare.calfare(minutesextended))
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
                    try:
                        SQL="select parkingstartdate,parkingenddate,parkingfare,extract(epoch from (parkingenddate-parkingstartdate) / 60 ) from "+ parking_table + " where uid in ('" + uid + "') and parkedcarregno in ('"+carregno+"') and parkingemail in ('"+str(parkingemail)+"')"
                        cur.execute(SQL)
                        result=cur.fetchall()
                    
                        parkingStartDate=result[0][0]
                        parkingEndDate=result[0][1]
                        parkingfare=result[0][2]
                        parkingtime_temp=result[0][3]
                        parkingtime_new=parkingtime_temp+int(minutesextended)
                        parkingfare_new=parking_fare.calfare(parkingtime_new)
                    except:
                        status="error"
                        status_who=statuswho.NO_DATA_TO_DISPLAY
                        
                    SQL="update tbl_parkdetails set parkingfare='"+ str(parkingfare_new) +"',parkingenddate=(parkingenddate+interval '1' minute * '"+ str(minutesextended)+ "') where parkingactive='1' and parkedcarregno in ('"+str(carregno)+"') and parkingemail in ('"+str(parkingemail)+"')"
                    cur.execute(SQL)
                    status="success"
                    status_who=statuswho.PARKING_SUCCESSFUL
                    jsonresult={"parkingFare":parkingfare_new}
                    #result=cur.fetchall()
                except:
                    status="error"
                    status_who=statuswho.UPDATE_DATA_FAILED
            conn.commit()
            conn.close()
        except:
            status="error"
            status_who=statuswho.TABLE_DOESNOT_EXIST
    if result==[]:
            result=-1
    return retcommon_status.createJSONResponse(status,status_who,jsonresult)


if __name__=="__main__":
    app.run(port=5000,debug=True)