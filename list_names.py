import sys
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\孙先生\aionclaw\project\health-guide'
with open(base + r'\data-full.js', 'r', encoding='utf-8') as f:
    c = f.read()

# 提取所有疾病名称
import re
names = re.findall(r"name:\s*'([^']+)'", c)
for i, n in enumerate(names):
    print(f'{i+1}. {n}')
print(f'\nTotal: {len(names)} diseases')
