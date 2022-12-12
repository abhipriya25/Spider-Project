import requests
import json
import csv

url = "https://api.mtsbank.ru/sp-geo-info-http/GetObjectList?fiasId=0c5b2444-70a0-4932-980c-b4dc0d3f02b5"

header = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Client-id": "portal2-web",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=header)
response = response.content.decode("utf-8").replace("'", '"')

data = json.loads(response)
data_object = {'object': []}
checking_list = ['Терминал МТС Банк', 'Банкомат МТС Банк', 'Офис Банка']
for object in data['object']:

    if object['type'] in checking_list:
        try:
            data_object["object"].append({
                "fullAddress":object["fullAddress"],
                "lat":object["lat"],
                "long":object["long"]
            })
        except KeyError:
            data_object["object"].append({
                "fullAddress":object["name"],
                "lat":object["lat"],
                "long":object["long"]
            })

with open("data_csv.csv", "w", encoding="utf-8") as file:
    csv_w = csv.writer(file)
    for emp in data_object['object']:
        csv_w.writerow([str(emp['fullAddress']), str(emp['lat']), str(emp['long'])])

with open("data.json", "w") as file:
    json.dump(data_object, file) # ensure_ascii = False - Убрать ASCII символы

with open("data_utf8.json", "w", encoding="utf-8") as file:
    json.dump(data_object, file, ensure_ascii=False) # ensure_ascii = False - Убрать ASCII символы