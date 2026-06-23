import sys, os, re, subprocess
sys.stdout.reconfigure(encoding='utf-8')
base = r'C:\Users\孙先生\aionclaw\project\health-guide'
with open(base + r'\index.html','r',encoding='utf-8') as f:
    html = f.read()
m = re.search(r"id:\s*'gallstone'.*?name:\s*'([^']+)'.*?brief:\s*'([^']+)'.*?explain:\s*'([^']+)'.*?daily:\s*\[(.*?)\].*?diet:\s*\[(.*?)\].*?medication:\s*\[(.*?)\].*?warning:\s*'([^']+)'", html, re.DOTALL)
if m:
    name,brief,explain,daily,diet,med,warning = m.groups()
    def cl(s):
        return '。'.join(re.findall(r"'([^']*)'", s))
    text = f'{name}。{brief}。通俗解释：{explain}。日常注意事项：{cl(daily)}。饮食和运动建议：{cl(diet)}。用药指导：{cl(med)}。就医预警信号：{warning}'
    print(f'Text length: {len(text)} chars')
    out = os.path.join(base, 'audio', 'gallstone.mp3')
    r = subprocess.run(['edge-tts','--voice','zh-CN-XiaoxiaoNeural','--rate=-10%','--text',text,'--write-media',out],capture_output=True,text=True,timeout=60)
    if r.returncode==0:
        print(f'OK: {os.path.getsize(out)} bytes')
    else:
        print('FAIL:', r.stderr[:200])
