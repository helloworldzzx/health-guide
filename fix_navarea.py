import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\孙先生\aionclaw\project\health-guide\index.html', 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace("getElementById('navArea')", "getElementById('categoryNav')")
with open(r'C:\Users\孙先生\aionclaw\project\health-guide\index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed navArea refs, count:', c.count("getElementById('categoryNav')"))
