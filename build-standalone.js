// build-standalone.js - 构建完整的单文件 HTML
const fs = require('fs');
const path = require('path');
const base = __dirname;

// ── 1. 读取 index.html ──
let html = fs.readFileSync(path.join(base, 'index.html'), 'utf8');

// ── 2. 读取 app.js ──
const appJS = fs.readFileSync(path.join(base, 'app.js'), 'utf8');

// ── 3. 读取 data.js 并提取原始12种疾病 ──
let dataContent = fs.readFileSync(path.join(base, 'data.js'), 'utf8');
// 截断在 expand-data.js 内容之前（原始 data.js 末尾是 IBS 条目后跟 ];）
const expandStart = dataContent.indexOf('\n,\n// expand-data.js');
if (expandStart > -1) {
  dataContent = dataContent.substring(0, expandStart);
}
// 确保以 ]; 结尾
dataContent = dataContent.replace(/,\s*$/, '');
if (!dataContent.trim().endsWith('];')) {
  dataContent = dataContent.trimEnd() + '\n];';
}

// ── 4. 读取 expand-data.js 并修复 ──
let expandContent = fs.readFileSync(path.join(base, 'expand-data.js'), 'utf8');

// 提取 newDiseases 数组内容
const arrayStart = expandContent.indexOf('const newDiseases = [');
if (arrayStart > -1) {
  expandContent = expandContent.substring(arrayStart + 'const newDiseases = ['.length);
}
// 移除末尾的 ];
expandContent = expandContent.replace(/\];\s*$/, '');

// 截断在 fattyliver 开始之前
const fattyIdx = expandContent.lastIndexOf("{id:'fattyliver'");
if (fattyIdx > -1) {
  expandContent = expandContent.substring(0, fattyIdx);
}

// ── 5. 补全脂肪肝数据 ──
const fattyLiverEntry = `{id:'fattyliver',category:'stomach',icon:'🫄',iconClass:'stomach',name:'脂肪肝',brief:'肝脏里堆积了太多脂肪，是最常见的肝病，很多人是体检发现的。',explain:'肝脏是人体的"化工厂"，正常情况下肝脏里也有少量脂肪。但如果脂肪堆积太多（超过肝脏重量的5%），就成了脂肪肝。主要原因有：吃得太油腻、喝酒太多、肥胖、糖尿病。大多数脂肪肝没有明显症状，但如果不控制，可能发展成肝炎、肝硬化，甚至肝癌。好消息是，早期脂肪肝是完全可以逆转的！',daily:['戒酒！酒精性脂肪肝必须滴酒不沾','控制体重，减重5%-10%，肝脏脂肪可减少30%以上','少吃油腻食物和甜食，控制总热量摄入','定期复查肝功能、B超，监测脂肪肝变化','不要乱吃"保肝药"或保健品，有些反而伤肝','如果有糖尿病或高血脂，要同时控制好'],diet:['多吃：绿叶蔬菜、水果、全谷物、豆制品','多吃：深海鱼、橄榄油（含健康脂肪）','少吃：油炸食品、肥肉、动物内脏、奶油蛋糕','绝对戒酒：酒精直接伤肝','少喝含糖饮料，果糖会直接在肝脏转化为脂肪','运动：快走、慢跑、游泳，每周至少150分钟','有氧运动+力量训练结合效果更好'],medication:['目前没有专门治疗脂肪肝的特效药','减肥和运动是最有效的"药物"','如果转氨酶持续升高，医生可能会用保肝药','维生素E对部分非酒精性脂肪肝患者可能有效，但需医生评估','不要相信"排毒养肝"保健品，大多没有科学依据','如果伴有糖尿病或高血脂，控制好这些疾病有助于改善脂肪肝'],warning:'如果出现：右上腹胀痛不适、乏力、食欲下降、皮肤或眼睛发黄（黄疸）——这些可能是脂肪肝加重的信号，需要及时就医。如果体检发现转氨酶持续升高，也要进一步检查。脂肪肝长期不控制可能发展成肝硬化，一定要重视！'}`;

// 组合完整疾病数据
const completeDiseases = dataContent.trimEnd().replace(/\];\s*$/, '') + ',\n' + expandContent.trim() + ',\n' + fattyLiverEntry + '\n];';

// 验证
const idCount = (completeDiseases.match(/id:'/g) || []).length;
console.log('Total disease entries:', idCount);

// ── 6. 构建内联 JS ──
// 语音搜索 CSS
const voiceCSS = `
/* ── 语音按钮 ── */
.voice-btn {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 38px;
  height: 38px;
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
  margin-top: 6px;
  min-height: 20px;
  transition: opacity 0.3s;
}
.search-wrap { position: relative; }
.search-input { padding-right: 52px; }

/* ── 语音朗读按钮 ── */
.speak-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 12px;
  border-radius: 50px;
  border: 1.5px solid var(--sage);
  background: var(--sage-light);
  color: var(--sage-dark);
  cursor: pointer;
  font-size: 0.8rem;
  font-family: var(--font-body);
  transition: var(--transition);
  margin-left: 10px;
  vertical-align: middle;
  white-space: nowrap;
}
.speak-btn:hover { background: var(--sage); color: white; }
.speak-btn.speaking {
  background: var(--cinnabar);
  color: white;
  border-color: var(--cinnabar);
  animation: pulse-voice 1s ease-in-out infinite;
}
`;

// 插入语音 CSS（在 @media print 之前）
html = html.replace('@media print {', voiceCSS + '\n\n@media print {');

// ── 7. 语音搜索 HTML 元素 ──
html = html.replace(
  '<input type="text" class="search-input" id="searchInput" placeholder="搜索疾病名称或症状…" autocomplete="off">',
  '<input type="text" class="search-input" id="searchInput" placeholder="搜索疾病名称或症状…" autocomplete="off">\n    <button class="voice-btn" id="voiceSearchBtn" title="语音搜索" aria-label="语音搜索">🎤</button>'
);

// 添加语音状态提示
html = html.replace(
  '</div>\n</div>\n\n<nav class="category-nav"',
  '</div>\n  <div class="voice-status" id="voiceStatus"></div>\n</div>\n\n<nav class="category-nav"'
);

// ── 8. 添加新分类按钮 ──
const newCategoryButtons = `
  <button class="category-btn" data-category="metabolic"><span class="icon">🧬</span>代谢性疾病</button>
  <button class="category-btn" data-category="respiratory"><span class="icon">🫁</span>呼吸系统</button>
  <button class="category-btn" data-category="nerve"><span class="icon">🧠</span>神经系统</button>
  <button class="category-btn" data-category="bone"><span class="icon">🦴</span>骨关节</button>
  <button class="category-btn" data-category="tumor"><span class="icon">🔬</span>肿瘤</button>
  <button class="category-btn" data-category="mental"><span class="icon">💙</span>精神心理</button>
  <button class="category-btn" data-category="sensory"><span class="icon">👁️</span>感官</button>
  <button class="category-btn" data-category="urinary"><span class="icon">🚻</span>泌尿生殖</button>`;

// 在最后一个分类按钮后插入新按钮（在 </nav> 之前）
html = html.replace(
  '<button class="category-btn" data-category="stomach"><span class="icon">🍽️</span>胃肠病</button>',
  '<button class="category-btn" data-category="stomach"><span class="icon">🍽️</span>胃肠病</button>\n  ' + newCategoryButtons
);

// ── 9. 新增分类图标样式 ──
const newIconCSS = `
.disease-icon.metabolic { background: #F0E6F6; }
.disease-icon.respiratory { background: #E6F0F6; }
.disease-icon.nerve { background: #F6F0E6; }
.disease-icon.bone { background: #F6E6E6; }
.disease-icon.tumor { background: #E6F6F0; }
.disease-icon.mental { background: #E6E6F6; }
.disease-icon.sensory { background: #F6F6E6; }
.disease-icon.urinary { background: #F0F6E6; }`;

html = html.replace('.disease-icon.stomach { background: var(--ochre-light); }', 
  '.disease-icon.stomach { background: var(--ochre-light); }\n' + newIconCSS);

// ── 10. 微信 Open Graph 标签 ──
const ogTags = `
<meta property="og:title" content="健康掌中宝 · 中老年常见病指南">
<meta property="og:description" content="高血压、冠心病、糖尿病、中风等30+种常见病，一看就懂的通俗指南。支持语音搜索和语音朗读。">
<meta property="og:type" content="article">
<meta property="og:site_name" content="健康掌中宝">
<meta name="description" content="中老年常见病通俗指南，涵盖心脑血管、代谢、消化、呼吸、骨关节、神经、精神心理、感官、泌尿生殖、肿瘤等类目，支持语音搜索和朗读。">
<meta name="keywords" content="健康,中老年,常见病,高血压,糖尿病,冠心病,中风,养生,语音,朗读">`;
html = html.replace('</head>', ogTags + '\n</head>');

// ── 11. 语音功能 JS ──
const voiceJS = `

// ========== 语音搜索功能 ==========
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

  recognition.onstart = function() {
    isListening = true;
    voiceSearchBtn.classList.add('listening');
    voiceSearchBtn.textContent = '🔴';
    voiceStatus.textContent = '正在听您说话…';
  };

  recognition.onresult = function(event) {
    var transcript = event.results[0][0].transcript.trim();
    searchInput.value = transcript;
    searchQuery = transcript;
    renderDiseases();
    voiceStatus.textContent = '已识别："' + transcript + '"';
    setTimeout(function() {
      var firstCard = document.querySelector('.disease-card');
      if (firstCard) {
        var cardId = firstCard.id.replace('card-', '');
        toggleCard(cardId);
      }
    }, 500);
  };

  recognition.onerror = function(event) {
    voiceStatus.textContent = '语音识别失败：' + (event.error === 'not-allowed' ? '请允许使用麦克风' : '请重试');
    stopListening();
  };

  recognition.onend = function() {
    stopListening();
  };

  voiceSearchBtn.addEventListener('click', function() {
    if (isListening) {
      recognition.stop();
    } else {
      voiceStatus.textContent = '';
      recognition.start();
    }
  });
} else {
  voiceSearchBtn.style.display = 'none';
  voiceStatus.textContent = '您的浏览器不支持语音功能';
}

function stopListening() {
  isListening = false;
  voiceSearchBtn.classList.remove('listening');
  voiceSearchBtn.textContent = '🎤';
}

// ========== 语音朗读功能 ==========
function speakDisease(diseaseId) {
  var d = null;
  for (var i = 0; i < diseases.length; i++) {
    if (diseases[i].id === diseaseId) { d = diseases[i]; break; }
  }
  if (!d) return;

  window.speechSynthesis.cancel();

  var text = d.name + '。' + d.brief + '。通俗解释：' + d.explain + '。日常注意事项：' + d.daily.join('。') + '。饮食和运动建议：' + d.diet.join('。') + '。用药指导：' + d.medication.join('。') + '。就医预警信号：' + d.warning;

  var utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = 'zh-CN';
  utterance.rate = 0.85;
  utterance.pitch = 1.0;

  var voices = window.speechSynthesis.getVoices();
  var zhVoice = null;
  for (var j = 0; j < voices.length; j++) {
    if (voices[j].lang.indexOf('zh-CN') === 0 || voices[j].lang.indexOf('zh-TW') === 0 || voices[j].lang.indexOf('zh') === 0) {
      zhVoice = voices[j];
      break;
    }
  }
  if (zhVoice) utterance.voice = zhVoice;

  var btn = document.getElementById('speak-btn-' + diseaseId);
  if (btn) {
    btn.classList.add('speaking');
    btn.textContent = '🔊 朗读中…';
  }

  utterance.onend = function() {
    if (btn) {
      btn.classList.remove('speaking');
      btn.textContent = '🔊 听语音';
    }
  };

  utterance.onerror = function() {
    if (btn) {
      btn.classList.remove('speaking');
      btn.textContent = '🔊 听语音';
    }
  };

  window.speechSynthesis.speak(utterance);
}

// 修改渲染函数，在每个疾病名称旁添加朗读按钮
var _originalRenderDiseases = renderDiseases;
renderDiseases = function() {
  _originalRenderDiseases();
  var nameEls = document.querySelectorAll('.disease-name');
  for (var i = 0; i < nameEls.length; i++) {
    var el = nameEls[i];
    var section = el.closest('.disease-section');
    if (!section) continue;
    var diseaseId = section.dataset.id;
    if (!document.getElementById('speak-btn-' + diseaseId)) {
      var btn = document.createElement('button');
      btn.id = 'speak-btn-' + diseaseId;
      btn.className = 'speak-btn';
      btn.textContent = '🔊 听语音';
      btn.title = '语音朗读';
      btn.onclick = (function(id) {
        return function(e) {
          e.stopPropagation();
          speakDisease(id);
        };
      })(diseaseId);
      el.appendChild(btn);
    }
  }
};

// 预加载语音列表
if (window.speechSynthesis) {
  window.speechSynthesis.getVoices();
  window.speechSynthesis.onvoiceschanged = function() {
    window.speechSynthesis.getVoices();
  };
}
`;

// ── 12. 替换外部引用为内联 ──
const combinedJS = completeDiseases + '\n' + appJS + '\n' + voiceJS;
html = html.replace(
  '<script src="data.js"></script>\n<script src="app.js"></script>',
  '<script>\n' + combinedJS + '\n</script>'
);

// ── 13. 写入输出文件 ──
const outPath = path.join(base, 'health-guide-standalone.html');
fs.writeFileSync(outPath, html, 'utf8');
console.log('Done! Written to:', outPath);
console.log('Size:', (fs.statSync(outPath).size / 1024).toFixed(1), 'KB');
