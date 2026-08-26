import requests
import os
from dotenv import load_dotenv

load_dotenv('world-quant-brain-mcp/.env')
s = requests.Session()
s.auth = (os.environ['CREDENTIALS_EMAIL'], os.environ['CREDENTIALS_PASSWORD'])

# 查询提交状态
r = s.get('https://api.worldquantbrain.com/alphas/78jZmqJO/submit')
print(f'GET /alphas/78jZmqJO/submit')
print(f'Status Code: {r.status_code}')
print(f'Body: {r.text[:1000]}')
print()

# 查询 alpha 详情
r2 = s.get('https://api.worldquantbrain.com/alphas/78jZmqJO')
print(f'GET /alphas/78jZmqJO')
print(f'Status Code: {r2.status_code}')
data = r2.json()
print(f'Status: {data.get("status")}')
print(f'Stage: {data.get("stage")}')
print(f'Date Submitted: {data.get("dateSubmitted")}')
print(f'Checks: {data.get("checks")}')
