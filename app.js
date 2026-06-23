// ── 应用逻辑 ──

const container = document.getElementById('diseaseContainer');
const searchInput = document.getElementById('searchInput');
const categoryNav = document.getElementById('categoryNav');
const backToTop = document.getElementById('backToTop');

let currentCategory = 'all';
let searchQuery = '';

// ── 渲染疾病卡片 ──
function renderDiseases() {
  let filtered = diseases;

  // 分类过滤
  if (currentCategory !== 'all') {
    filtered = filtered.filter(d => d.category === currentCategory);
  }

  // 搜索过滤
  if (searchQuery.trim()) {
    const q = searchQuery.trim().toLowerCase();
    filtered = filtered.filter(d => {
      const searchText = (d.name + d.brief + d.explain + d.daily.join('') + d.diet.join('') + d.medication.join('') + d.warning).toLowerCase();
      return searchText.includes(q);
    });
  }

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="no-results">
        <span class="no-icon">🔎</span>
        <p>没有找到相关内容</p>
        <p style="font-size:0.82rem;margin-top:4px;">试试换个关键词，或者选择其他分类</p>
      </div>
    `;
    return;
  }

  container.innerHTML = filtered.map((d, i) => `
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
    </div>
  `).join('');
}

// ── 展开/收起卡片 ──
function toggleCard(id) {
  const card = document.getElementById('card-' + id);
  card.classList.toggle('expanded');
}

// ── 分类切换 ──
categoryNav.addEventListener('click', (e) => {
  const btn = e.target.closest('.category-btn');
  if (!btn) return;

  document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');

  currentCategory = btn.dataset.category;
  renderDiseases();
});

// ── 搜索 ──
let searchTimer;
searchInput.addEventListener('input', () => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => {
    searchQuery = searchInput.value;
    renderDiseases();
  }, 300);
});

// ── 回到顶部 ──
function updateBackToTop() {
  if (window.scrollY > 500) {
    backToTop.classList.add('visible');
  } else {
    backToTop.classList.remove('visible');
  }
}

window.addEventListener('scroll', updateBackToTop, { passive: true });

backToTop.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

// ── 初始渲染 ──
renderDiseases();
