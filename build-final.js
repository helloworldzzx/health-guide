// build-final.js - 生成最终单文件 HTML（含语音功能 + 微信 OG 标签）
const fs = require('fs');
const path = require('path');

const dir = 'C:/Users/孙先生/aionclaw/project/health-guide';

// 读取文件
let html = fs.readFileSync(path.join(dir, 'index.html'), 'utf8');
const dataJS = fs.readFileSync(path.join(dir, 'data.js'), 'utf8');
const appJS = fs.readFileSync(path.join(dir, 'app.js'), 'utf8');

// 1. 添加微信 OG 标签
const ogTags = `
<meta property="og:title" content="健康掌中宝 · 中老年常见病指南">
<meta property="og:description" content="高血压、糖尿病、冠心病、中风等33种常见病，一看就懂的通俗指南">
<meta property="og:type" content="article">
<meta property="og:site_name" content="健康掌中宝">
<meta name="description" content="中老年常见病通俗指南，涵盖心脑血管、代谢、消化、呼吸、骨关节、神经、精神心理、感官、泌尿、肿瘤等类目">`;

html = html.replace('</head>', ogTags + '\n</head>');

// 2. 替换外部 JS 引用为内联
html = html.replace(
  '<script src="data.js"></script>\n<script src="app.js"></script>',
  '<script>\n' + dataJS + '\n' + appJS + '\n</script>'
);

// 3. 添加语音搜索按钮的 CSS（在 Print 之前）
const voiceCSS = `
/* 语音按钮 */
.voice-btn {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: var(--sage-light);
  color: var(--sage-dark);
  cursor: pointer;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
  z-index: 2;
}
.voice-btn:hover { background: var(--sage); color: white; }
.voice-btn.listening {
  background: var(--cinnabar);
  color: white;
  animation: pulse-voice 1s ease-in-out infinite;
}
@keyframes pulse-voice {
  0%, 100% { box-shadow: 0 0 0 0 rgba(199,91,58,0.3); }
  50% { box-shadow: 0 0 0 12px rgba(199,91,58,0); }
}
.voice-status {
  text-align: center;
  font-size: 0.82rem;
  color: var(--cinnabar);
  margin-top: 8px;
  min-height: 20px;
}
.search-wrap { position: relative; }
.search-input { padding-right: 48px; }

/* 语音朗读按钮 */
.speak-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 12px;
  border-radius: 50px;
  border: 1px solid var(--sage);
  background: var(--sage-light);
  color: var(--sage-dark);
  cursor: pointer;
  font-size: 0.8rem;
  font-family: var(--font-body);
  transition: var(--transition);
  margin-left: 8px;
  vertical-align: middle;
}
.speak-btn:hover { background: var(--sage); color: white; }
.speak-btn.speaking {
  background: var(--cinnabar);
  color: white;
  border-color: var(--cinnabar);
  animation: pulse-voice 1s ease-in-out infinite;
}`;

html = html.replace('/* ── Print ── */', voiceCSS + '\n\n/* ── Print ── */');

// 4. 在搜索框添加语音按钮
html = html.replace(
  '<input type="text" class="search-input" id="searchInput" placeholder="搜索疾病名称或症状…" autocomplete="off">',
  '<input type="text" class="search-input" id="searchInput" placeholder="搜索疾病名称或症状…" autocomplete="off">\n    <button class="voice-btn" id="voiceSearchBtn" title="语音搜索">🎤</button>'
);

// 5. 添加语音状态提示
html = html.replace('</div>\n</div>\n\n<nav', '</div>\n  <div class="voice-status" id="voiceStatus"></div>\n</div>\n\n<nav');

// 6. 添加新分类标签
html = html.replace(
  '<button class="category-btn" data-category="stomach">\n    <span class="icon">🍽️</span>胃肠病\n  </button>',
  `<button class="category-btn" data-category="stomach"><span class="icon">🍽️</span>消化系统</button>
  <button class="category-btn" data-category="metabolic"><span class="icon">⚡</span>代谢</button>
  <button class="category-btn" data-category="respiratory"><span class="icon">🫁</span>呼吸</button>
  <button class="category-btn" data-category="nerve"><span class="icon">🧬</span>神经</button>
  <button class="category-btn" data-category="bone"><span class="icon">🦴</span>骨关节</button>
  <button class="category-btn" data-category="mental"><span class="icon">💙</span>心理</button>
  <button class="category-btn" data-category="sensory"><span class="icon">👁️</span>感官</button>
  <button class="category-btn" data-category="urinary"><span class="icon">🚻</span>泌尿</button>
  <button class="category-btn" data-category="tumor"><span class="icon">🔬</span>肿瘤</button>`
);

// 7. 添加语音功能 JS（在 </script> 之前）
const voiceJS = `

// ========== 语音搜索 ==========
const voiceSearchBtn = document.getElementById('voiceSearchBtn');
const voiceStatus = document.getElementById('voiceStatus');
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = null;
let isListening = false;

if (SpeechRecognition) {
  recognition = new SpeechRecognition();
  recognition.lang = 'zh-CN';
  recognition.continuous = false;
  recognition.interimResults = false;

  recognition.onstart = () => {
    isListening = true;
    voiceSearchBtn.classList.add('listening');
    voiceSearchBtn.textContent = '🔴';
    voiceStatus.textContent = '正在听您说话…';
  };

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript.trim();
    searchInput.value = transcript;
    searchQuery = transcript;
    renderDiseases();
    voiceStatus.textContent = '已识别：' + transcript;
    setTimeout(() => {
      const firstCard = document.querySelector('.disease-card');
      if (firstCard) {
        const cardId = firstCard.id.replace('card-', '');
        toggleCard(cardId);
      }
    }, 500);
  };

  recognition.onerror = (event) => {
    voiceStatus.textContent = '语音识别失败：' + (event.error === 'not-allowed' ? '请允许使用麦克风' : '请重试');
    stopListening();
  };

  recognition.onend = () => { stopListening(); };

  voiceSearchBtn.addEventListener('click', () => {
    if (isListening) { recognition.stop(); }
    else { voiceStatus.textContent = ''; recognition.start(); }
  });
} else {
  voiceSearchBtn.style.display = 'none';
}

function stopListening() {
  isListening = false;
  voiceSearchBtn.classList.remove('listening');
  voiceSearchBtn.textContent = '🎤';
}

// ========== 语音朗读 ==========
function speakDisease(diseaseId) {
  const d = diseases.find(d => d.id === diseaseId);
  if (!d) return;
  window.speechSynthesis.cancel();
  const text = d.name + '。' + d.brief + '。通俗解释：' + d.explain + '。日常注意事项：' + d.daily.join('。') + '。饮食和运动建议：' + d.diet.join('。') + '。用药指导：' + d.medication.join('。') + '。就医预警信号：' + d.warning;
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = 'zh-CN';
  utterance.rate = 0.85;
  utterance.pitch = 1.0;
  const voices = window.speechSynthesis.getVoices();
  const zhVoice = voices.find(v => v.lang.startsWith('zh-CN') || v.lang.startsWith('zh-TW') || v.lang.startsWith('zh'));
  if (zhVoice) utterance.voice = zhVoice;
  const btn = document.getElementById('speak-btn-' + diseaseId);
  if (btn) { btn.classList.add('speaking'); btn.textContent = '🔊 朗读中…'; }
  utterance.onend = () => { if (btn) { btn.classList.remove('speaking'); btn.textContent = '🔊 听语音'; } };
  utterance.onerror = () => { if (btn) { btn.classList.remove('speaking'); btn.textContent = '🔊 听语音'; } };
  window.speechSynthesis.speak(utterance);
}

// 重写渲染函数，添加朗读按钮
const _origRender = renderDiseases;
renderDiseases = function() {
  _origRender();
  document.querySelectorAll('.disease-name').forEach(el => {
    const section = el.closest('.disease-section');
    if (!section) return;
    const diseaseId = section.dataset.id;
    if (!document.getElementById('speak-btn-' + diseaseId)) {
      const btn = document.createElement('button');
      btn.id = 'speak-btn-' + diseaseId;
      btn.className = 'speak-btn';
      btn.textContent = '🔊 听语音';
      btn.title = '语音朗读';
      btn.onclick = (e) => { e.stopPropagation(); speakDisease(diseaseId); };
      el.appendChild(btn);
    }
  });
};

if (window.speechSynthesis) {
  window.speechSynthesis.getVoices();
  window.speechSynthesis.onvoiceschanged = () => { window.speechSynthesis.getVoices(); };
}`;

// 在 </script> 之前插入语音 JS
html = html.replace('renderDiseases();\n</script>', 'renderDiseases();' + voiceJS + '\n</script>');

// 写入
const outPath = path.join(dir, 'index.html');
fs.writeFileSync(outPath, html, 'utf8');
console.log('Done! Written to:', outPath);
console.log('Size:', (fs.statSync(outPath).size / 1024).toFixed(1), 'KB');
