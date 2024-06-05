import requests

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

json_data = {
    'MSSubClass': 60,
    'MSZoning': 'RL',
    'LotArea': 7844,
    'LotConfig': 'Inside',
    'BldgType': '1Fam',
    'OverallCond': 7,
    'YearBuilt': 1978,
    'YearRemodAdd': 1978,
    'Exterior1st': 'HdBoard',
    'BsmtFinSF2': 0,
    'TotalBsmtSF': 672,
}

response = requests.post('http://localhost:30001/predict', headers=headers, json=json_data)
if response.status_code == 200:
    print("Successful!")
    print(response.json())
else:
    print("Failed to get prediction!")