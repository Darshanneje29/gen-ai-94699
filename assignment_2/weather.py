import requests
import json
from challenge.secret import api_key
city = str(input("Enter city name: "))
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

response = requests.get(url)
data = response.json()

print(f"Weather in {city}:")
print("Temperature:", data['main']['temp'], "°C")
print("Weather:", data['weather'][0]['description'])
print("Humidity:", data['main']['humidity'], "%")