import sys
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\孙先生\aionclaw\project\health-guide'

with open(base + r'\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the voice JS section end - after speechSynthesis setup, before </script>
old_end = '''if (window.speechSynthesis) {
  window.speechSynthesis.getVoices();
  window.speechSynthesis.onvoiceschanged = function() { window.speechSynthesis.getVoices(); };
}'''

new_end = '''if (window.speechSynthesis) {
  window.speechSynthesis.getVoices();
  window.speechSynthesis.onvoiceschanged = function() { window.speechSynthesis.getVoices(); };
}

// 重新渲染以添加语音朗读按钮
renderDiseases();'''

html = html.replace(old_end, new_end)

with open(base + r'\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Done! Size:', len(html))
print('Contains "重新渲染以添加语音朗读按钮":', '重新渲染以添加语音朗读按钮' in html)
