import requests
import json
panel = input("Введите адрес панели (с http(s)://): ")
url = f'{panel}/api/application/servers'
key = input("Введите ключ API: ")
loks = []
while True:
    loki = input("Введите имя локаций, которые чистить, для продолжения введите STOP: ")
    if loki != "STOP":
        loks.append(loki)
    if loki == "STOP":
        break
headers = {

    "Authorization": f"Bearer {key}",

    "Accept": "application/json",

    "Content-Type": "application/json",

}

response = requests.request('GET', url, headers=headers)
sss = json.loads(response.text)
lists = sss['data']
for i in range(2, sss['meta']['pagination']['total_pages'] + 1):
    print(i)
    response2 = json.loads(requests.request('GET', f'{panel}/api/application/servers?page={i}', headers=headers).text)['data']
    lists += response2
l = 0
for ss in lists:
    if ss['attributes']['container']['environment']['P_SERVER_LOCATION'] in loks:
        l += 1

print("Серверов к удалению: " + str(l) + " из " + str(len(lists)))
yes = input("Продолжить? y/n ")
if yes == "y":
    for ss in lists:
        if ss['attributes']['container']['environment']['P_SERVER_LOCATION'] in loks:
            url = f'{panel}/api/application/servers/{ss["attributes"]["id"]}/force'
            response = requests.request('DELETE', url, headers=headers)
    print("Готово!")
else:
    print("Галя, отмена!")
