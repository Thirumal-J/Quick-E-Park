from flask import Flask
import psycopg2
import json
from flask import request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app=Flask(__name__)

DB_HOST="192.168.99.100"
DB_NAME="QuickEPark"
DB_USER="postgres"
DB_PASS="Pass@123"


User_table="Users"

@app.route("/")
def index():
    return "Hello!! This is reset password api"

@app.route("/resetpassword",methods=['POST'])
def resetpassword():
    result=-1
    try:
        conn =psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST)
        cur=conn.cursor()
        
        try:
            Username=request.json["User"]["Username"]
        except:
            print("Exception input user format")

        SQL="select email from "+ User_table +" where Username in ('"+ Username +"')"
        
        try:
            cur.execute(SQL)
            result=cur.fetchall()
        except:
            print("Table doesn't exist or null values found")
        if result==[]:
            result=0
        else:
            result=result[0][0]
            SendEmail(result)
        conn.commit()
        conn.close()
    except:
        print("Exception")
    return str(result)

def SendEmail(EmailId):
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


if __name__=="__main__":
    app.run(port=5001,debug=True)