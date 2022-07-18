import requests
import pandas as pd

url = "https://api.mtsbank.ru/sp-geo-info-http/GetObjectList?fiasId=0c5b2444-70a0-4932-980c-b4dc0d3f02b5"
headers = {
    "Client-id": "portal2-web",
    }
    

response = requests.get(url, headers=headers)

data = response.json()['object']
df = pd.DataFrame(data)
df.to_csv('MTC.csv')
df.head()
