import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\孙先生\aionclaw\project\health-guide\index.html', 'r', encoding='utf-8') as f:
    c = f.read()
m = re.search(r'<script>(.*?)</script>', c, re.DOTALL)
if m:
    js = m.group(1)
    print('JS length:', len(js))
    opens = js.count('{')
    closes = js.count('}')
    print('Braces:', opens, closes, 'diff:', opens-closes)
    parens_open = js.count('(')
    parens_close = js.count(')')
    print('Parens:', parens_open, parens_close, 'diff:', parens_open-parens_close)
    # Check last 500 chars
    print('Last 500 chars:')
    print(js[-500:])
