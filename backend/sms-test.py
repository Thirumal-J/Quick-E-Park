# we import the Twilio client from the dependency we just installed
from twilio.rest import Client

# the following line needs your Twilio Account SID and Auth Token
client = Client("AC78efa0ff62d4ffc031f0dc1d057fbd4c", "c9e1603577f8e90724253366cf84cc3e")

# change the "from_" number to your Twilio number and the "to" number
# to the phone number you signed up for Twilio with, or upgrade your
# account to send SMS to any phone number
client.messages.create(to="+4915214463267", 
                       from_="+17655133192", 
                       body="Hello from Thiru!")