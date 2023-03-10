import requests
import json
import pandas as pd
import boto3
import matplotlib.pyplot as plt

urldol = "https://bank.gov.ua/NBU_Exchange/exchange_site?start=20210101&end=20211231&valcode=usd&sort=exchangedate&order=asc&json"
urleur = "https://bank.gov.ua/NBU_Exchange/exchange_site?start=20210101&end=20211231&valcode=eur&sort=exchangedate&order=asc&json"
response = requests.get(urldol)
data = response.json()

with open("dol.json", "w") as f1:
    json.dump(data, f1)
dol = pd.read_json('dol.json')
dol.to_excel('dol.xlsx', index=False)

response = requests.get(urleur)
data = response.json()

with open("eur.json", "w") as f2:
    json.dump(data, f2)
eur = pd.read_json('eur.json')
eur.to_excel('eur.xlsx', index=False)

dolex = pd.read_excel('dol.xlsx')
eurex = pd.read_excel('eur.xlsx')

merg = pd.concat([dolex, eurex], ignore_index=False, axis=1)

merg.to_excel('merg.xlsx', index=False)

df = pd.read_excel('merg.xlsx')
df.to_csv('merg.csv', index=False)

s3 = boto3.client('s3', aws_access_key_id='AKIAWBC6MDSEQWXKC4PQ', aws_secret_access_key='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')
with open('merg.csv', 'rb') as f:
    s3.upload_fileobj(f, 'lab2kos', 'mergm.csv')

s3.download_file('lab2kos','mergm.csv','mergm.csv')

# загрузка данных из CSV-файла
data = pd.read_csv('mergm.csv')


# выбор столбцов по номеру
x = data.iloc[:, 0]
y1 = data.iloc[:, 5]
y2 = data.iloc[:, 15]

# построение графика
plt.plot(x, y1)
plt.plot(x, y2)
plt.show()

plt.savefig('graph.png')
with open('graph.png', 'rb') as f:
    s3.upload_fileobj(f, 'lab2kos', 'graph.png')