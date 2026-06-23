import os

base = r'C:\Users\孙先生\aionclaw\project\health-guide'

# Read original data.js
with open(os.path.join(base, 'data.js'), 'r', encoding='utf-8') as f:
    data_content = f.read()

# Read expand-data.js (new diseases)
with open(os.path.join(base, 'expand-data.js'), 'r', encoding='utf-8') as f:
    expand_content = f.read()

# Find the closing ]; in data.js
end_pos = data_content.rfind('];')
if end_pos == -1:
    print('ERROR: cannot find end of array')
    exit()

# Insert new diseases before the ];
new_content = data_content[:end_pos] + ',\n' + expand_content.strip() + '\n];'

# Write back
with open(os.path.join(base, 'data.js'), 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f'Done. New data.js size: {len(new_content)} bytes')
count = new_content.count("id: '")
print(f'Disease count: ~{count}')
