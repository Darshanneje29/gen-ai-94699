import requests
import json

url = "https://jsonplaceholder.typicode.com/users"

response = requests.get(url)

data = response.json()  
    
with open("users.json", "w") as f:
    json.dump(data, f, indent=4)  
        
print("Status code:", response.status_code)
