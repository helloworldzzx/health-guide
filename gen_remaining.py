# gen_remaining.py - 生成剩余15个完整版音频
import subprocess, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\孙先生\aionclaw\project\health-guide'
audio_dir = os.path.join(base, 'audio')
os.makedirs(audio_dir, exist_ok=True)

with open(os.path.join(base, 'index.html'), 'r', encoding='utf-8') as f:
    html = f.read()

# 提取所有疾病
pattern = r"id:\s*'([^']+)'.*?name:\s*'([^']+)'.*?brief:\s*'([^']+)'.*?explain:\s*'([^']+)'.*?daily:\s*\[(.*?)\].*?diet:\s*\[(.*?)\].*?medication:\s*\[(.*?)\].*?warning:\s*'([^']+)'"
matches = re.findall(pattern, html, re.DOTALL)

print(f'Found {len(matches)} diseases')

for i, (did, name, brief, explain, daily, diet, med, warning) in enumerate(matches):
    out_file = os.path.join(audio_dir, f'{did}.mp3')
    # Check if file exists and is > 100KB (full version)
    if os.path.exists(out_file) and os.path.getsize(out_file) > 100000:
        print(f'[{i+1}/{len(matches)}] SKIP {name} (exists, {os.path.getsize(out_file)} bytes)')
        continue
    
    # Clean up the text
    def clean_list(s):
        items = re.findall(r"'([^']*)'", s)
        return '。'.join(items)
    
    daily_text = clean_list(daily)
    diet_text = clean_list(diet)
    med_text = clean_list(med)
    
    text = f'{name}。{brief}。通俗解释：{explain}。日常注意事项：{daily_text}。饮食和运动建议：{diet_text}。用药指导：{med_text}。就医预警信号：{warning}'
    
    print(f'[{i+1}/{len(matches)}] Generating {name} ({len(text)} chars)...')
    
    r = subprocess.run([
        'edge-tts',
        '--voice', 'zh-CN-XiaoxiaoNeural',
        '--rate=-10%',
        '--text', text,
        '--write-media', out_file
    ], capture_output=True, text=True, timeout=60)
    
    if r.returncode == 0:
        size = os.path.getsize(out_file)
        print(f'  OK: {size} bytes')
    else:
        print(f'  FAIL: {r.stderr[:200]}')

print('\nDone!')
