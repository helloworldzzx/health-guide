#!/usr/bin/env python3
"""Parse existing index.html to extract full text for each disease, then generate MP3 audio files using edge-tts.
Voice: zh-CN-XiaoxiaoNeural, rate: -10%
"""
import subprocess
import os
import re
import sys
import time

audio_dir = r'C:\Users\孙先生\aionclaw\project\health-guide\audio'
os.makedirs(audio_dir, exist_ok=True)

html_path = r'C:\Users\孙先生\aionclaw\project\health-guide\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Extract diseases data from the JS array
# Find the diseases array
match = re.search(r'const diseases = \[(.*?)\];', html, re.DOTALL)
if not match:
    print("ERROR: Could not find diseases array in HTML")
    sys.exit(1)

diseases_js = match.group(1)

# Parse each disease object - extract id, name, brief, explain, daily, diet, medication, warning
# Use a simple parser that finds each object by id pattern
disease_blocks = re.findall(r"\{[^}]*?id:\s*'([^']+)'[^}]*?\}", diseases_js, re.DOTALL)

# Better approach: extract each disease block
# Split by "id:" pattern
blocks = re.split(r"(?=\{)", diseases_js)
disease_data = []

for block in blocks:
    if not block.strip() or not re.search(r"id:\s*'", block):
        continue
    
    # Extract fields
    id_match = re.search(r"id:\s*'([^']+)'", block)
    name_match = re.search(r"name:\s*'([^']+)'", block)
    brief_match = re.search(r"brief:\s*'([^']+)'", block)
    explain_match = re.search(r"explain:\s*'([^']+)'", block)
    
    # Extract arrays (daily, diet, medication)
    def extract_array(field_name, text):
        # Find the array for this field
        pattern = rf"{field_name}:\s*\[(.*?)\]"
        match = re.search(pattern, text, re.DOTALL)
        if not match:
            return []
        arr_text = match.group(1)
        items = re.findall(r"'([^']*)'", arr_text)
        return items
    
    # Extract warning (could be string or array)
    warning_match = re.search(r"warning:\s*'([^']+)'", block)
    
    if not id_match or not name_match:
        continue
    
    d_id = id_match.group(1)
    d_name = name_match.group(1)
    d_brief = brief_match.group(1) if brief_match else ''
    d_explain = explain_match.group(1) if explain_match else ''
    d_daily = extract_array('daily', block)
    d_diet = extract_array('diet', block)
    d_medication = extract_array('medication', block)
    d_warning = warning_match.group(1) if warning_match else ''
    
    # Build full text for TTS
    parts = [f"{d_name}。{d_brief}。{d_explain}"]
    
    if d_daily:
        parts.append("日常注意事项：" + "。".join(d_daily) + "。")
    if d_diet:
        parts.append("饮食和运动建议：" + "。".join(d_diet) + "。")
    if d_medication:
        parts.append("用药指导：" + "。".join(d_medication) + "。")
    if d_warning:
        parts.append("预警信号：" + d_warning + "。")
    
    full_text = "。".join(parts)
    # Clean up: remove multiple periods, extra spaces
    full_text = re.sub(r'。{2,}', '。', full_text)
    full_text = re.sub(r'\s+', '', full_text)
    
    disease_data.append({
        'id': d_id,
        'name': d_name,
        'text': full_text
    })
    print(f"  Parsed: {d_id} ({d_name}) - {len(full_text)} chars")

print(f"\nTotal diseases parsed: {len(disease_data)}")

# Generate audio files
total = len(disease_data)
for i, d in enumerate(disease_data):
    output_path = os.path.join(audio_dir, f"{d['id']}.mp3")
    
    # Check if file already exists and is recent
    if os.path.exists(output_path):
        print(f"[{i+1}/{total}] SKIP {d['id']} - already exists")
        continue
    
    print(f"[{i+1}/{total}] Generating {d['id']} ({d['name']})...")
    
    # edge-tts command
    cmd = [
        'edge-tts',
        '--voice', 'zh-CN-XiaoxiaoNeural',
        '--rate=-10%',
        '--text', d['text'],
        '--write-media', output_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            print(f"  ERROR: {result.stderr}")
        else:
            size = os.path.getsize(output_path)
            print(f"  OK: {size} bytes")
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT for {d['id']}")
    except Exception as e:
        print(f"  EXCEPTION: {e}")
    
    # Small delay to avoid overwhelming the TTS service
    time.sleep(1)

print("\nDone!")
