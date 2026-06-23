import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\孙先生\aionclaw\project\health-guide\index.html', 'r', encoding='utf-8') as f:
    c = f.read()
# Remove all debug console.log lines
c = re.sub(r"console\.log\(\"[^\"]+\"\);\n", '', c)
print(f'Removed debug lines. Size: {len(c)}')
with open(r'C:\Users\孙先生\aionclaw\project\health-guide\index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done')
