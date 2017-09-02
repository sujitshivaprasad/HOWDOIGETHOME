import googlemaps
from datetime import datetime
from twilio.rest import TwilioRestClient
from HTMLParser import HTMLParser
from dotenv import load_dotenv
import os

# Setup the directory so I can load the .env file
BASE_DIR = (os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Initialization
how_to_go = []

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

gmaps = googlemaps.Client(key='AIzaSyB08XoTl1mP8UFDegpBq8mZ2NSbN8_Trn4')

# Setup account settings and required values
# Your Account SID from twilio.com/console
account_sid = os.getenv('ACCOUNT_SID')
# Your Auth Token from twilio.com/console
auth_token = os.getenv('AUTH_TOKEN')
origin = os.getenv('ORIGIN')
destination = os.getenv('DESTINATION')

client = TwilioRestClient(account_sid, auth_token) 
now=datetime.now()

# Get details from Google Maps API
dir=gmaps.directions(origin=origin, destination=destination, mode='driving', departure_time=now, traffic_model='best_guess')

# Store what I want (time taken)
time_taken = dir[0]['legs'][0]['duration_in_traffic']['text']
summary = dir[0]['summary']

# Remove the HTML tags
for item in (dir[0]['legs'][0]['steps']):
    s = MLStripper()
    s.feed(item['html_instructions'])
    how_to_go.append(s.get_data())

# Convert list to string
how_i_really_need_to_go = '.  '.join(how_to_go)

# Send myself some instructions for the day
instructions = "Today's best route is by taking %s, and it'll take %s. Here's how you can get there: %s." % (summary, time_taken, how_i_really_need_to_go)
print instructions
# Now send it!
# message = client.messages.create(
# to="+15125251405", 
# from_="+15127142914",
# body=instructions)

# print(message.sid)