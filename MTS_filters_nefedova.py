import requests
import pandas as pd

url = "https://api.mtsbank.ru/sp-geo-info-http/GetObjectList?fiasId=0c5b2444-70a0-4932-980c-b4dc0d3f02b5"
headers = {
    "Client-id": "portal2-web",
    }
    

response = requests.get(url, headers=headers)


print(response.json()['object'])



for row in response.json()['object']:
  print(row['id'])
  print(row['lat'])
  print(row['long'])
  print(row['name'])
  print(row['schedule'])
  print(row['fullAddress'])
  print('\n')