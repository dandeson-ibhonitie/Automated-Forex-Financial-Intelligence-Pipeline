
import requests
import json
from fake_useragent import UserAgent



url = "https://open.er-api.com/v6/latest/USD" # The dedicated public open data server path 



ua = UserAgent() #
custom_headers = {'User-Agent': ua.random}

response = requests.get(url, headers= custom_headers)
response.raise_for_status()

   
data = response.json()

with open ("raw_rates.json", "w") as file: #Saving the unedited raw backup  file
    json.dump(data, file, indent = 4)

print("extraction sucessful")