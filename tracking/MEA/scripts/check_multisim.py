import requests
from pathlib import Path

env_path = Path('world-quant-brain-mcp/.env')
config = {}
with open(env_path) as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            k, v = line.strip().split('=', 1)
            config[k] = v.strip('"')

auth = (config['CREDENTIALS_EMAIL'], config['CREDENTIALS_PASSWORD'])
base_url = 'https://api.worldquantbrain.com'

for ms_id in ['1NvPlgd5o4vBbxqPEHkoaOx', 'Zuv59emn4j5cpE1aWFxGAlO']:
    resp = requests.get(f'{base_url}/simulations/{ms_id}', auth=auth)
    print(f'{ms_id}: HTTP {resp.status_code}')
    if resp.status_code == 200:
        data = resp.json()
        status = data.get('status', 'N/A')
        progress = data.get('progress', 'N/A')
        print(f'  Status: {status}')
        print(f'  Progress: {progress}')
        if 'children' in data:
            print(f'  Children: {len(data["children"])}')
            for child in data['children'][:3]:
                print(f'    - {child}')
