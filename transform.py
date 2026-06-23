# transform.py - 改造 HTML: 顶部折叠 + 广告位
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\孙先生\aionclaw\project\health-guide'
with open(base + r'\index_backup.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ============ 1. 添加折叠顶部栏 CSS ============
fold_css = '''
/* ── 折叠顶部栏 ── */
.foldable-top { transition: all 0.4s ease; overflow: hidden; }
.foldable-top.collapsed { max-height: 0 !important; padding-top: 0 !important; padding-bottom: 0 !important; margin: 0 !important; opacity: 0; pointer-events: none; }
.sticky-minibar { position: fixed; top: 0; left: 0; right: 0; z-index: 100; background: var(--cream); padding: 10px 16px; display: flex; align-items: center; gap: 10px; box-shadow: var(--shadow-md); transform: translateY(-100%); transition: transform 0.35s ease; }
.sticky-minibar.visible { transform: translateY(0); }
.sticky-minibar .back-arrow { font-size: 1.3rem; cursor: pointer; padding: 4px 8px; border: none; background: var(--sage-light); color: var(--sage-dark); border-radius: 8px; }
.sticky-minibar .current-title { font-family: var(--font-display); font-size: 1.05rem; font-weight: 700; color: var(--ink); flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
/* 广告位 */
.ad-placeholder { border: 2px dashed #d0c8b8; background: rgba(245,237,224,0.6); border-radius: var(--radius-sm); display: flex; align-items: center; justify-content: center; color: var(--ink-muted); font-size: 0.78rem; margin: 12px 16px; padding: 16px; text-align: center; }
.ad-placeholder.banner { height: 80px; max-width: 640px; margin-left: auto; margin-right: auto; }
.ad-placeholder.feed { height: 60px; margin: 20px 16px; }
.ad-placeholder.bottom { height: 80px; max-width: 640px; margin-left: auto; margin-right: auto; }'''

html = html.replace('/* ── Print ── */', fold_css + '\n\n/* ── Print ── */')

# ============ 2. 改造 header 为可折叠 ============
html = html.replace('<header class="header">', '<header class="header foldable-top" id="topArea">')
html = html.replace('</header>', '</header>\n\n<!-- 折叠顶栏 -->\n<div class="sticky-minibar" id="minibar">\n  <button class="back-arrow" id="backBtn" title="返回列表">✕</button>\n  <span class="current-title" id="minibarTitle"></span>\n</div>')

# ============ 3. 改造 nav 为可折叠 ============
html = html.replace('<nav class="category-nav"', '<nav class="category-nav foldable-top" id="navArea"')

# ============ 4. 在 nav 后面加 banner 广告位 ============
html = html.replace('</nav>\n\n<main', '</nav>\n\n<div class="ad-placeholder banner">📢 广告位 640×80</div>\n\n<main')

# ============ 5. 在 footer 前面加底部广告位 ============
html = html.replace('<footer class="footer">', '<div class="ad-placeholder bottom">📢 广告位 640×80</div>\n\n<footer class="footer">')

# ============ 6. 修改 toggleCard 函数，添加折叠逻辑 ============
new_toggle = '''function toggleCard(id) {
  var card = document.getElementById('card-' + id);
  var isExpanded = card.classList.contains('expanded');
  
  // 先关闭所有卡片
  document.querySelectorAll('.disease-card.expanded').forEach(function(c) {
    if (c.id !== 'card-' + id) c.classList.remove('expanded');
  });
  
  if (isExpanded) {
    // 收起：恢复顶部
    card.classList.remove('expanded');
    document.getElementById('topArea').classList.remove('collapsed');
    document.getElementById('navArea').classList.remove('collapsed');
    document.getElementById('minibar').classList.remove('visible');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  } else {
    // 展开：折叠顶部
    card.classList.add('expanded');
    var d = diseases.find(function(d) { return d.id === id; });
    document.getElementById('minibarTitle').textContent = d ? d.name : '';
    document.getElementById('topArea').classList.add('collapsed');
    document.getElementById('navArea').classList.add('collapsed');
    document.getElementById('minibar').classList.add('visible');
    // 滚动到卡片
    setTimeout(function() {
      card.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
  }
}'''

html = html.replace(
    '''function toggleCard(id) {
  var card = document.getElementById('card-' + id);
  card.classList.toggle('expanded');
}''',
    new_toggle
)

# ============ 7. 返回按钮 ============
back_js = '''
// 返回按钮
document.getElementById('backBtn').addEventListener('click', function() {
  var expandedCard = document.querySelector('.disease-card.expanded');
  if (expandedCard) {
    var cardId = expandedCard.id.replace('card-', '');
    toggleCard(cardId);
  }
});'''

html = html.replace('// ── 初始渲染 ──', back_js + '\n\n// ── 初始渲染 ──')

# ============ 8. 每5个疾病插入广告位 ============
# 在 renderDiseases 函数中修改
old_render_end = "container.innerHTML = filtered.map((d, i) => `"
new_render_start = '''container.innerHTML = filtered.map(function(d, i) {
    var cardHtml = `
    <div class="disease-section" style="animation-delay:${i * 0.06}s" data-id="${d.id}">
      <div class="disease-card" id="card-${d.id}">
        <div class="disease-header" onclick="toggleCard('${d.id}')">
          <div class="disease-icon ${d.iconClass}">${d.icon}</div>
          <div class="disease-header-left">
            <div class="disease-name">${d.name}</div>
            <div class="disease-brief">${d.brief}</div>
          </div>
          <div class="expand-indicator">▼</div>
        </div>
        <div class="disease-detail">
          <div class="detail-inner">
            <div class="info-block explain">
              <div class="info-block-title"><span class="dot"></span>这是什么病？（通俗解释）</div>
              <p>${d.explain}</p>
            </div>
            <div class="info-block daily">
              <div class="info-block-title"><span class="dot"></span>日常注意事项和自我管理</div>
              <ul>${d.daily.map(item => `<li>${item}</li>`).join('')}</ul>
            </div>
            <div class="info-block diet">
              <div class="info-block-title"><span class="dot"></span>饮食和运动建议</div>
              <ul>${d.diet.map(item => `<li>${item}</li>`).join('')}</ul>
            </div>
            <div class="info-block medication">
              <div class="info-block-title"><span class="dot"></span>用药指导和注意事项</div>
              <ul>${d.medication.map(item => `<li>${item}</li>`).join('')}</ul>
            </div>
            <div class="info-block warning">
              <div class="info-block-title"><span class="dot"></span>⚠️ 需要就医的预警信号</div>
              <div class="warning-alert">
                <span class="alert-icon">🚨</span>
                <span>${d.warning}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>`;
    // 每5个卡片插入广告
    if ((i + 1) % 5 === 0 && i < filtered.length - 1) {
      cardHtml += '<div class="ad-placeholder feed">📢 广告位 640×60</div>';
    }
    return cardHtml;
  }).join('');'''

# Find and replace the render section
# The original uses template literals with backticks
old_pattern = r"container\.innerHTML = filtered\.map\(\(d, i\) => `[\s\S]*?`\n  \)\.join\(''\);"
match = re.search(old_pattern, html)
if match:
    html = html[:match.start()] + new_render_start + html[match.end():]
    print('Replaced render function successfully')
else:
    print('WARNING: Could not find render pattern')

# ============ 9. 更新语音按钮的 onclick 也触发折叠 ============
# doSpeak 函数不需要改，音频路径已经是 audio/xxx.mp3

# Write
with open(base + r'\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Done! Size: {len(html)} bytes')
for chk in ['collapsed','minibar','backBtn','ad-placeholder','banner','feed','foldable-top','sticky-minibar']:
    print(f'{chk}: {html.count(chk)}')
