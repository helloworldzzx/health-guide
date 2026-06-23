import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\孙先生\aionclaw\project\health-guide\index.html', 'r', encoding='utf-8') as f:
    c = f.read()
pos = c.find('<script>')
debug = '\nconsole.log("SCRIPT STARTED");\n'
c = c[:pos+8] + debug + c[pos+8:]
pos2 = c.find('// \u2500\u2500 初始渲染 \u2500\u2500')
c = c[:pos2] + 'console.log("ABOUT TO RENDER");\n' + c[pos2:]
with open(r'C:\Users\孙先生\aionclaw\project\health-guide\index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done')
