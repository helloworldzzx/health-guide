import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\孙先生\aionclaw\project\health-guide\index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Add debug at multiple points
# After diseases array
pos = c.find('// ── 状态')
c = c[:pos] + 'console.log("DISEASES LOADED, count=" + diseases.length);\n' + c[pos:]

# After category buttons
pos = c.find('currentCategory = btn.dataset.category;')
c = c[:pos] + 'console.log("CATEGORY BTNS BOUND");\n  ' + c[pos:]

# Before backBtn
pos = c.find("// 返回按钮 - 收起卡片恢复顶部")
c = c[:pos] + 'console.log("BEFORE BACKBTN");\n' + c[pos:]

# After backBtn IIFE
pos = c.find('// ── 初始渲染 ──')
c = c[:pos] + 'console.log("AFTER BACKBTN");\n' + c[pos:]

with open(r'C:\Users\孙先生\aionclaw\project\health-guide\index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Debug v2 done')
