import sys, re
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\孙先生\aionclaw\project\health-guide'

# 读取原始 data.js（12种疾病）
with open(base + r'\data.js', 'r', encoding='utf-8') as f:
    orig = f.read()

# 读取 expand-data.js
with open(base + r'\expand-data.js', 'r', encoding='utf-8') as f:
    expand = f.read()

# 从 expand 中提取所有完整的疾病条目（以 {id: 开头，以 } 结尾的）
# 去掉文件头的 JS 代码和注释
# 找到第一个 {id:
first_entry = expand.find('{id:')
if first_entry < 0:
    print('ERROR: no entries found')
    sys.exit(1)

# 提取所有完整条目（以 }, 或 }] 结尾的）
entries_text = expand[first_entry:]
# 找到最后一个完整的条目（被截断的 fattyliver 之前）
# 找到倒数第二个 }, 之后的位置
# 简单方法：找到最后一个 }, 然后去掉不完整的部分
last_complete = entries_text.rfind('},')
if last_complete > 0:
    # 保留到最后一个完整条目
    entries_text = entries_text[:last_complete+1]  # 保留到 }

print('Extracted entries text length:', len(entries_text))
print('Entries count:', entries_text.count("{id:"))

# 合并：orig 去掉最后的 ]; 加上 , 加上新条目 加上 ];
end_pos = orig.rfind('];')
merged = orig[:end_pos] + ',\n' + entries_text + '\n];'

# 写入
out_path = base + r'\data-full.js'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(merged)

print('Merged size:', len(merged))
print('Total diseases:', merged.count("{id:"))
print('Written to:', out_path)
