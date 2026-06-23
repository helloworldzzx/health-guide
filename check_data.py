import os

base = r'C:\Users\孙先生\aionclaw\project\health-guide'
with open(os.path.join(base, 'data-full.js'), 'r', encoding='utf-8') as f:
    c = f.read()

last_brace = c.rfind('}')
print('Last } at position', last_brace, 'of', len(c))
print('LAST 300 chars:')
print(c[-300:])
