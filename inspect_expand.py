import sys
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\孙先生\aionclaw\project\health-guide'
with open(base + r'\expand-data.js', 'r', encoding='utf-8') as f:
    c = f.read()

print('Lines:', c.count('\n'))
print('id counts:', c.count("id:'"))
print('First 500:')
print(c[:500])
print('---')
print('Last 500:')
print(c[-500:])
