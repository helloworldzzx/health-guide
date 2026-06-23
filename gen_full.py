# gen_full.py - 生成完整 data.js
import os

base = r'C:\Users\孙先生\aionclaw\project\health-guide'

# 读取原始 data.js
with open(os.path.join(base, 'data.js'), 'r', encoding='utf-8') as f:
    orig = f.read()

# 找到 ]; 位置
end_pos = orig.rfind('];')
existing = orig[:end_pos]  # 保留到 ]; 之前

# 新疾病数据从文件读取
with open(os.path.join(base, 'expand-data.js'), 'r', encoding='utf-8') as f:
    expand = f.read()

# 去掉 expand 文件开头的 node.js 代码，只保留数据部分
# 找到第一个 { 
data_start = expand.find('{')
if data_start > 0:
    expand = expand[data_start:]

# 合并
new_content = existing + ',\n' + expand.strip() + '\n];'

# 写入
out_path = os.path.join(base, 'data-full.js')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f'Written: {out_path}')
print(f'Size: {len(new_content)} bytes')
# Count diseases
import re
count = len(re.findall(r"id:\s*'", new_content))
print(f'Disease count: {count}')
