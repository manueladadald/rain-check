import requests
from twilio.rest import Client
import data

MY_LAT = data.MY_LAT
MY_LONG = data.MY_LONG
MY_KEY = data.MY_KEY
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall?"
twilio_sid = data.twilio_sid
twilio_token = data.twilio_token
twilio_number = data.twilio_number
account_sid = twilio_sid
auth_token = twilio_token

parameters = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": MY_KEY,
    "exclude": "current,minutely,daily",
}

response = requests.get(OWM_Endpoint, params=parameters)
response.raise_for_status()

data = response.json()
# data["hourly"][n]["weather"][0]["id"]
weather_slice = data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if condition_code <= 700:
        will_rain = True

if will_rain:
    print("Bring an umbrella! ☔")
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It's going to rain today! Bring an umbrella! ☔",
        from_=twilio_number,
        to=data.phone_number
    )

    print(message.status)
