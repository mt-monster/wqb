import requests
import json

# 从 config.json 读取凭证
config = json.load(open(r'C:\Users\MENGTAO\.qoder-cn\skills\brain-makeSomeGem\scripts\headless_runner\config.json'))
email = config['brain_email']
password = config['brain_password']
auth = (email, password)

# 3 个候选的 alpha ID
alpha_ids = ['LL7dldJL', 'ak7EWE9x', 'O07x5xXd']

for alpha_id in alpha_ids:
    print(f"\n{'='*80}")
    print(f"Alpha ID: {alpha_id}")
    print(f"{'='*80}")
    
    # 获取 alpha 详情
    url = f'https://api.worldquantbrain.com/alphas/{alpha_id}'
    r = requests.get(url, auth=auth)
    
    if r.status_code == 200:
        data = r.json()
        
        # 显示基本信息
        print(f"\n基本信息:")
        print(f"  Status: {data.get('status')}")
        print(f"  Code: {data.get('code', '')[:80]}...")
        
        # 显示 IS 检查结果
        is_checks = data.get('is', {})
        print(f"\nIS 检查:")
        print(f"  Sharpe: {is_checks.get('sharpe')}")
        print(f"  Fitness: {is_checks.get('fitness')}")
        print(f"  Turnover: {is_checks.get('turnover')}")
        print(f"  Margin: {is_checks.get('margin')}")
        
        # 显示失败的检查
        failed_checks = is_checks.get('failedChecks', [])
        print(f"\n失败的检查 ({len(failed_checks)}):")
        for check in failed_checks:
            print(f"  - {check}")
        
        # 显示 description
        regular = data.get('regular', {})
        description = regular.get('description', '')
        print(f"\nDescription 长度: {len(description)} 字符")
        if description:
            print(f"Description 预览: {description[:200]}...")
        else:
            print("Description: (空)")
    else:
        print(f"HTTP {r.status_code}: {r.text[:200]}")
