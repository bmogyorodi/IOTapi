import requests
import json
from flask import Flask, request
url="https://api.us-east-1.mbedcloud.com/v2/subscriptions/017837ed8bad000000000001001066b7/3200/0/4401"
headers={'content-type': 'application/json','authorization': 'Bearer ak_2MDE3NzA3MzI5MDg5N2VlMDkzZTNkNzRjMDAwMDAwMDA017838004e346634c22452aa00000000I0rtjjyMoU1HLdpsKp3Wmv2EtsAKD9iu'}
response = requests.put(url=url,headers=headers)
print(response.content)

url="https://api.us-east-1.mbedcloud.com/v2/notification/callback"
data={'url':'http://127.0.0.1/2333/webhook'}
response = requests.put(url=url,data=json.dumps(data),headers=headers)
print(response.content)



