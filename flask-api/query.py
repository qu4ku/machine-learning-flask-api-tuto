import json
import requests
import pandas as pd

# Setting the headers to send and accept json responses
header = {
	'Content-Type': 'application/json',
	'Accept': 'application/json'
}

# Reading test batch
df = pd.read_csv('../data/test.csv')
df = df.head()
# Convertin to json
data = df.to_json(orient='records')

print(data)

# POST <url>/predict

resp = requests.post(
	'http://0.0.0.0:8000/predict',
	data=json.dumps(data),
	headers=header
	)
print(resp.status_code)

# The final response:
print(resp.json())
