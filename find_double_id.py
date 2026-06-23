import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\孙先生\aionclaw\project\health-guide\index.html', 'r', encoding='utf-8') as f:
    c = f.read()
pos = c.find('id="navArea" id="categoryNav"')
if pos > 0:
    print('FOUND double id at pos', pos)
    print(repr(c[pos-50:pos+80]))
else:
    print('NOT FOUND')
    # Search for navArea
    pos2 = c.find('navArea')
    print('navArea at', pos2, repr(c[pos2-20:pos2+80]))
