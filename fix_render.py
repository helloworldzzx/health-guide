import re

with open(r'C:\Users\孙先生\aionclaw\project\health-guide\index.html', 'r', encoding='utf-8') as f:
    c = f.read()

start = c.find('container.innerHTML = filtered.map((d, i) =>')
end_marker = ").join('');"
end = c.find(end_marker, start)
end += len(end_marker)

old_block = c[start:end]
print(f'Block length: {len(old_block)}')

new_block = """container.innerHTML = filtered.map(function(d, i) {
    var cardHtml = '<div class="disease-section" style="animation-delay:' + (i * 0.06) + 's" data-id="' + d.id + '"><div class="disease-card" id="card-' + d.id + '"><div class="disease-header" onclick="toggleCard(\\'' + d.id + '\\')"><div class="disease-icon ' + d.iconClass + '">' + d.icon + '</div><div class="disease-header-left"><div class="disease-name">' + d.name + '</div><div class="disease-brief">' + d.brief + '</div></div><div class="expand-indicator">▼</div></div><div class="disease-detail"><div class="detail-inner"><div class="info-block explain"><div class="info-block-title"><span class="dot"></span>这是什么病？（通俗解释）</div><p>' + d.explain + '</p></div><div class="info-block daily"><div class="info-block-title"><span class="dot"></span>日常注意事项和自我管理</div><ul>' + d.daily.map(function(item) { return '<li>' + item + '</li>'; }).join('') + '</ul></div><div class="info-block diet"><div class="info-block-title"><span class="dot"></span>饮食和运动建议</div><ul>' + d.diet.map(function(item) { return '<li>' + item + '</li>'; }).join('') + '</ul></div><div class="info-block medication"><div class="info-block-title"><span class="dot"></span>用药指导和注意事项</div><ul>' + d.medication.map(function(item) { return '<li>' + item + '</li>'; }).join('') + '</ul></div><div class="info-block warning"><div class="info-block-title"><span class="dot"></span>⚠️ 需要就医的预警信号</div><div class="warning-alert"><span class="alert-icon">🚨</span><span>' + d.warning + '</span></div></div></div></div></div></div>';
    if ((i + 1) % 5 === 0 && i < filtered.length - 1) {
      cardHtml += '<div class="ad-placeholder feed">📢 广告位 640×60</div>';
    }
    return cardHtml;
  }).join('');"""

c = c[:start] + new_block + c[end:]

with open(r'C:\Users\孙先生\aionclaw\project\health-guide\index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print(f'Done! Size: {len(c)} bytes')
print(f'feed: {c.count("feed")}')
print(f'filtered.map(function: {c.count("filtered.map(function")}')
