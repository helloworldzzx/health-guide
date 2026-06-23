import sys, re
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\孙先生\aionclaw\project\health-guide'

# Read ORIGINAL data.js (the backup before any merges)
# Since data.js was already modified, use index.html's inline data... 
# Actually let's read the original 12 from the first version
# The original data.js has 12 diseases. But it's been overwritten.
# Let me reconstruct: read data-full.js and deduplicate

with open(base + r'\data-full.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Extract all disease entries between { and },
# deduplicate by id
seen_ids = set()
unique_entries = []

# Find all {...} blocks that contain id:
# Simple approach: split by '  {' and deduplicate
# Actually use regex to find each disease object
pattern = r'\{\s*id:\s*\'([^\']+)\''
matches = list(re.finditer(pattern, c))

# For each match, extract from its start to the matching }
# Simple approach: find }, after each id
entries = []
for m in matches:
    id_val = m.group(1)
    start = m.start()
    # Find the closing of this object - find the next '},' or '}]' after this id
    # Count braces
    depth = 0
    i = start
    while i < len(c):
        if c[i] == '{':
            depth += 1
        elif c[i] == '}':
            depth -= 1
            if depth == 0:
                entry = c[start:i+1]
                entries.append((id_val, entry))
                break
        i += 1

print(f'Found {len(entries)} entries total')

# Deduplicate
seen = set()
unique = []
for id_val, entry in entries:
    if id_val not in seen:
        seen.add(id_val)
        unique.append(entry)

print(f'Unique: {len(unique)}')

# Rebuild data.js
new_data = '// 健康掌中宝 - 完整疾病数据库\nconst diseases = [\n' + ',\n'.join(unique) + '\n];'

with open(base + r'\data.js', 'w', encoding='utf-8') as f:
    f.write(new_data)

print(f'Written data.js: {len(new_data)} bytes, {len(unique)} diseases')
for i, (id_val, _) in enumerate(zip(seen, unique)):
    print(f'{i+1}. {id_val}')
