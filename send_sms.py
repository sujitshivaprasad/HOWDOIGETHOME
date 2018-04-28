from twilio.rest import TwilioRestClient

# Your Account SID from twilio.com/console
account_sid = "ACe4dcd9385e0a3543a8f2a6798574478e"
# Your Auth Token from twilio.com/console
auth_token  = "5d55535a96dcfbf38fefea26d41d07fd"

client = TwilioRestClient(account_sid, auth_token)

message = client.messages.create(
    to="+15125251405", 
    from_="+15127142914",
    body="Hello from Python!")

print(message.sid)
