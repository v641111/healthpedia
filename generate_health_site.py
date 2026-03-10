#!/usr/bin/env python3
"""HealthPedia - Comprehensive Bilingual Health Encyclopedia Generator"""
import os, json, html, shutil
from pathlib import Path

SITE_NAME = "HealthPedia"
SITE_NAME_ZH = "健康百科"
DOMAIN = "https://v641111.github.io"
BASE = "/healthpedia"
OUT = "healthpedia-site"

# ============================================================
# CSS
# ============================================================
CSS = """:root{--bg:#f0f5fa;--bg2:#e4ecf4;--card:#fff;--bdr:#d0dbe6;--pri:#0077cc;--pri-d:#005fa3;--pri-l:#e6f2ff;--acc:#00a86b;--acc-l:#e6f7f0;--red:#dc3545;--red-l:#fdeaec;--warn:#f0a030;--warn-l:#fff8e6;--text:#1a2a3a;--text-m:#5a6b7c;--text-l:#8a9bac;--white:#fff}
*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Inter','Noto Sans SC',system-ui,sans-serif;background:var(--bg);color:var(--text);line-height:1.7;-webkit-font-smoothing:antialiased}
a{color:var(--pri);text-decoration:none;transition:color .2s}a:hover{color:var(--pri-d)}h1{font-size:clamp(28px,5vw,42px);font-weight:800;line-height:1.2;letter-spacing:-.02em}h2{font-size:24px;font-weight:700;margin-bottom:12px}h3{font-size:18px;font-weight:600;margin-bottom:8px}
.wrap{max-width:1100px;margin:0 auto;padding:0 20px}
.nav{position:sticky;top:0;z-index:100;background:rgba(255,255,255,.95);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);border-bottom:1px solid var(--bdr);box-shadow:0 1px 3px rgba(0,0,0,.04)}.nav-in{display:flex;align-items:center;justify-content:space-between;height:64px;max-width:1100px;margin:0 auto;padding:0 20px}
.logo{display:flex;align-items:center;gap:10px;font-weight:800;font-size:18px;color:var(--pri)}.logo-i{width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,var(--pri),var(--acc));display:flex;align-items:center;justify-content:center;color:#fff;font-size:14px;font-weight:700}
.nlinks{display:flex;gap:20px;align-items:center}.nlinks a{color:var(--text-m);font-size:14px;font-weight:500}.nlinks a:hover,.nlinks a.on{color:var(--pri)}
.lbtn{background:var(--pri-l);color:var(--pri);border:none;padding:6px 14px;border-radius:6px;font-size:12px;font-weight:600;cursor:pointer;text-decoration:none}
.mbtn{display:none;background:none;border:none;color:var(--text);font-size:24px;cursor:pointer}.mmenu{display:none;background:var(--card);border-top:1px solid var(--bdr);padding:16px 20px}.mmenu a{display:block;padding:10px 0;color:var(--text-m);font-size:14px}
.hero{background:linear-gradient(135deg,#0077cc 0%,#00a86b 100%);color:#fff;padding:80px 20px 60px;text-align:center;position:relative;overflow:hidden}.hero::before{content:'';position:absolute;inset:0;background:radial-gradient(circle at 1px 1px,rgba(255,255,255,.06) 1px,transparent 0);background-size:32px 32px}.hero h1{color:#fff;margin-bottom:16px;position:relative}.hero p{color:rgba(255,255,255,.85);font-size:18px;max-width:600px;margin:0 auto 32px;position:relative}
.hero2{background:linear-gradient(135deg,#0077cc,#0099dd);color:#fff;padding:48px 20px;text-align:center;position:relative}.hero2 h1{color:#fff;font-size:clamp(24px,4vw,36px)}.hero2 p{color:rgba(255,255,255,.8);margin-top:8px}
.card{background:var(--card);border:1px solid var(--bdr);border-radius:14px;padding:24px;transition:all .3s}.card:hover{box-shadow:0 8px 30px rgba(0,119,204,.08);transform:translateY(-3px);border-color:var(--pri)}
.g2{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}.g3{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}.g4{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:16px}
.sec{padding:60px 20px;max-width:1100px;margin:0 auto}.sec-a{background:var(--bg2);padding:60px 0}.sec h2{text-align:center}.sub{color:var(--text-m);text-align:center;margin-bottom:32px;font-size:15px}
.info-box{border-radius:12px;padding:20px 24px;margin:24px 0}.info-sym{background:var(--pri-l);border-left:4px solid var(--pri)}.info-prev{background:var(--acc-l);border-left:4px solid var(--acc)}.info-treat{background:#f3e8ff;border-left:4px solid #7c3aed}.info-warn{background:var(--red-l);border-left:4px solid var(--red)}
.info-box h3{margin-bottom:12px}.info-box ul{list-style:none;padding:0}.info-box li{padding:6px 0 6px 28px;position:relative;font-size:15px}.info-box li::before{content:'';position:absolute;left:4px;top:14px;width:8px;height:8px;border-radius:50%}.info-sym li::before{background:var(--pri)}.info-prev li::before{background:var(--acc)}.info-treat li::before{background:#7c3aed}.info-warn li::before{background:var(--red)}
.badge{display:inline-block;padding:4px 14px;border-radius:20px;font-size:11px;font-weight:600;letter-spacing:.03em}
.bc{display:flex;gap:8px;align-items:center;font-size:13px;color:var(--text-l);margin-bottom:24px;flex-wrap:wrap}.bc a{color:var(--text-m)}.bc a:hover{color:var(--pri)}
.tw{overflow-x:auto;border-radius:12px;border:1px solid var(--bdr);background:var(--card)}table{width:100%;border-collapse:collapse;font-size:14px}th{background:var(--pri-l);color:var(--pri-d);font-weight:600;font-size:11px;letter-spacing:.05em;text-transform:uppercase;padding:14px 16px;text-align:left}td{padding:14px 16px;border-bottom:1px solid var(--bg)}tr:hover td{background:var(--pri-l)}
.article{max-width:800px}.article-body p{margin-bottom:16px;font-size:16px;line-height:1.8}.article-body h3{margin-top:32px;color:var(--pri)}
.cat-icon{width:56px;height:56px;border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:28px;flex-shrink:0}
.age-card{background:var(--card);border:1px solid var(--bdr);border-radius:16px;padding:28px;text-align:center;transition:all .3s}.age-card:hover{border-color:var(--pri);box-shadow:0 8px 24px rgba(0,119,204,.08)}.age-emoji{font-size:48px;margin-bottom:12px}
.met{background:var(--card);border:1px solid var(--bdr);border-radius:10px;padding:18px;text-align:center}.met-v{font-size:28px;font-weight:800;color:var(--pri)}.met-l{font-size:12px;color:var(--text-m);margin-top:4px}
.btn{display:inline-block;background:var(--pri);color:#fff;padding:12px 28px;border-radius:8px;font-weight:600;font-size:14px;transition:all .3s;border:none;cursor:pointer}.btn:hover{background:var(--pri-d);color:#fff;transform:translateY(-2px);box-shadow:0 4px 16px rgba(0,119,204,.3)}
.btn-o{display:inline-block;background:transparent;color:var(--pri);border:1px solid var(--bdr);padding:12px 28px;border-radius:8px;font-weight:500;font-size:14px;transition:all .3s}.btn-o:hover{border-color:var(--pri);background:var(--pri-l)}
.disc{background:var(--warn-l);border:1px solid #ffe0a0;border-radius:12px;padding:20px 24px;margin-top:40px;font-size:13px;color:#8a6d00}
.tag-grid{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0}.tag-grid a{background:var(--pri-l);color:var(--pri);padding:6px 16px;border-radius:20px;font-size:13px;font-weight:500;transition:all .2s}.tag-grid a:hover{background:var(--pri);color:#fff}
footer{background:var(--white);border-top:1px solid var(--bdr);padding:40px 20px 24px}.fi{max-width:1100px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px}.fc{color:var(--text-l);font-size:11px}
.related{margin-top:48px;padding-top:32px;border-top:1px solid var(--bdr)}
@keyframes fadeup{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}.fu{animation:fadeup .6s ease both}.fd1{animation-delay:.1s}.fd2{animation-delay:.2s}
@media(max-width:768px){.nlinks{display:none!important}.mbtn{display:flex!important}.g2,.g3{grid-template-columns:1fr}.g4{grid-template-columns:repeat(2,1fr)}.hero h1{font-size:28px!important}.hero{padding:60px 20px 40px}.mmenu.open{display:block!important}.sec{padding:40px 16px}}
@media(max-width:500px){td,th{padding:10px;font-size:12px}.g4{grid-template-columns:1fr}}"""

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">'

# ============================================================
# CATEGORIES: (id, name_en, name_zh, emoji, color)
# ============================================================
CATS = [
    ("diseases","Common Diseases","常见疾病","🏥","#dc3545"),
    ("nutrition","Nutrition & Diet","营养饮食","🥗","#ff8c00"),
    ("fitness","Exercise & Fitness","运动健身","🏃","#00a86b"),
    ("mental","Mental Health","心理健康","🧠","#6f42c1"),
    ("maternal","Maternal & Child","母婴育儿","👶","#e83e8c"),
    ("senior","Senior Health","老年健康","🧓","#6c757d"),
    ("first-aid","First Aid","急救常识","🚑","#dc3545"),
    ("prevention","Preventive Care","预防保健","🛡️","#0066cc"),
    ("tcm","Traditional Chinese Medicine","中医养生","🌿","#28a745"),
    ("skin","Skin Health","皮肤健康","✨","#fd7e14"),
    ("eye","Eye Health","眼科健康","👁️","#17a2b8"),
    ("dental","Dental Health","口腔健康","🦷","#20c997"),
    ("heart","Cardiovascular","心血管健康","❤️","#dc3545"),
    ("digestive","Digestive Health","消化系统","🫄","#ffc107"),
    ("respiratory","Respiratory","呼吸系统","🫁","#17a2b8"),
    ("bone","Bone & Joint","骨骼关节","🦴","#6c757d"),
    ("sleep","Sleep Health","睡眠健康","😴","#6610f2"),
]
CAT_MAP = {c[0]: c for c in CATS}

# ============================================================
# ARTICLE HELPER
# ============================================================
def A(id, n, nz, d, dz, sym, symz, prev, prevz, treat, treatz, sev="varies", ages="all"):
    return dict(id=id, n=n, nz=nz, d=d, dz=dz,
        sym=sym.split("|"), symz=symz.split("|"),
        prev=prev.split("|"), prevz=prevz.split("|"),
        treat=treat.split("|"), treatz=treatz.split("|"),
        sev=sev, ages=ages)

# ============================================================
# PLACEHOLDER - Data will be loaded from data file
# ============================================================
from health_data import ALL_ARTICLES, AGE_GUIDES

# ============================================================
# UTILITY FUNCTIONS
# ============================================================
def e(s): return html.escape(str(s))

def nav(lang='en'):
    p = f'{BASE}/zh' if lang=='zh' else BASE
    lbl = {
        'cats': '健康百科' if lang=='zh' else 'Health A-Z',
        'age': '年龄指南' if lang=='zh' else 'Age Guide',
        'about': '关于' if lang=='zh' else 'About',
    }
    toggle = f'<a href="{BASE}/" class="lbtn">EN</a>' if lang=='zh' else f'<a href="{BASE}/zh/" class="lbtn">中文</a>'
    sn = SITE_NAME_ZH if lang=='zh' else SITE_NAME
    return f'''<nav class="nav"><div class="nav-in">
<a href="{p}/" class="logo"><span class="logo-i">H+</span>{sn}</a>
<div class="nlinks"><a href="{p}/categories/">{lbl['cats']}</a><a href="{p}/age-guide/">{lbl['age']}</a><a href="{p}/about.html">{lbl['about']}</a></div>
<div style="display:flex;gap:10px;align-items:center">{toggle}<button class="mbtn" onclick="document.getElementById('mm').classList.toggle('open')" aria-label="Menu">☰</button></div>
</div><div id="mm" class="mmenu"><a href="{p}/categories/">{lbl['cats']}</a><a href="{p}/age-guide/">{lbl['age']}</a><a href="{p}/about.html">{lbl['about']}</a></div></nav>'''

def footer(lang='en'):
    p = f'{BASE}/zh' if lang=='zh' else BASE
    yr = '2026'
    return f'''<div class="disc" style="max-width:800px;margin:40px auto"><strong>{"⚠️ 免责声明" if lang=="zh" else "⚠️ Disclaimer"}</strong><br>{"本网站内容仅供参考，不构成医疗建议。如有健康问题，请咨询专业医生。" if lang=="zh" else "This content is for informational purposes only and does not constitute medical advice. Please consult a healthcare professional for medical concerns."}</div>
<footer><div class="fi">
<div style="display:flex;align-items:center;gap:8px"><span class="logo-i" style="width:28px;height:28px;font-size:10px">H+</span><span style="font-weight:700;font-size:14px">{SITE_NAME_ZH if lang=="zh" else SITE_NAME}</span></div>
<nav style="display:flex;gap:20px;font-size:12px;color:var(--text-l)"><a href="{p}/categories/">{"健康百科" if lang=="zh" else "Health A-Z"}</a><a href="{p}/age-guide/">{"年龄指南" if lang=="zh" else "Age Guide"}</a><a href="{p}/about.html">{"关于" if lang=="zh" else "About"}</a></nav>
<div class="fc">© {yr} {SITE_NAME}. All rights reserved.</div></div></footer>'''

def head(title, desc, path, lang='en'):
    alt_path = f'{BASE}/zh{path[len(BASE):]}' if lang=='en' else BASE + path[len(f"{BASE}/zh"):]
    en_path = path if lang=='en' else alt_path
    zh_path = f'{BASE}/zh{path[len(BASE):]}' if lang=='en' else path
    return f'''<!DOCTYPE html><html lang="{"zh-CN" if lang=="zh" else "en"}"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc[:160])}">
<link rel="canonical" href="{DOMAIN}{path}">
<link rel="alternate" hreflang="en" href="{DOMAIN}{en_path}">
<link rel="alternate" hreflang="zh" href="{DOMAIN}{zh_path}">
<link rel="alternate" hreflang="x-default" href="{DOMAIN}{en_path}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc[:160])}">
<meta property="og:url" content="{DOMAIN}{path}"><meta property="og:type" content="website"><meta property="og:site_name" content="{SITE_NAME}">
<meta name="twitter:card" content="summary"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc[:160])}">
{FONTS}
<style>{CSS}</style>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-PLLR9YHTZ0"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-PLLR9YHTZ0');
</script>
</head><body>'''

def page(filepath, content):
    d = os.path.dirname(filepath)
    if d: os.makedirs(os.path.join(OUT, d), exist_ok=True)
    with open(os.path.join(OUT, filepath), 'w', encoding='utf-8') as f:
        f.write(content)

def breadcrumb_html(items, lang='en'):
    h = '<div class="bc">'
    for i,(name,url) in enumerate(items):
        if i > 0: h += ' <span>/</span> '
        if url: h += f'<a href="{url}">{e(name)}</a>'
        else: h += f'<span style="color:var(--text)">{e(name)}</span>'
    h += '</div>'
    return h

def breadcrumb_json(items):
    il = []
    for i,(n,u) in enumerate(items):
        it = {"@type":"ListItem","position":i+1,"name":n}
        if u: it["item"] = f"{DOMAIN}{u}"
        il.append(it)
    return f'<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":il})}</script>'

# ============================================================
# PAGE GENERATORS
# ============================================================

def gen_homepage(lang):
    is_zh = lang == 'zh'
    p = f'{BASE}/zh' if is_zh else BASE
    path = f'{p}/'
    prefix = f'{p}'
    title = f"{SITE_NAME_ZH} - 您的健康知识百科" if is_zh else f"{SITE_NAME} - Your Health Knowledge Encyclopedia"
    desc = "全面的中英文健康百科，涵盖常见疾病、营养、运动、心理健康等17个分类。" if is_zh else "Comprehensive bilingual health encyclopedia covering diseases, nutrition, fitness, mental health and 17 categories."

    h = head(title, desc, path, lang) + nav(lang)

    # Hero
    h += f'''<div class="hero"><div style="position:relative;z-index:1">
<div style="font-size:64px;margin-bottom:16px">🏥</div>
<h1>{SITE_NAME_ZH if is_zh else SITE_NAME}</h1>
<p>{"涵盖17个健康领域、全年龄段的综合医疗健康知识平台" if is_zh else "Comprehensive health knowledge platform covering 17 categories for all ages"}</p>
<div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap">
<a href="{prefix}/categories/" class="btn" style="background:#fff;color:var(--pri)">{"浏览健康百科" if is_zh else "Browse Health A-Z"}</a>
<a href="{prefix}/age-guide/" class="btn-o" style="border-color:rgba(255,255,255,.4);color:#fff">{"年龄健康指南" if is_zh else "Age Guide"}</a>
</div></div></div>'''

    # Stats bar
    total_articles = sum(len(v) for v in ALL_ARTICLES.values())
    h += f'''<div style="background:var(--card);border-bottom:1px solid var(--bdr);padding:20px"><div style="display:flex;justify-content:center;gap:48px;flex-wrap:wrap;max-width:800px;margin:0 auto;text-align:center">
<div><div style="font-size:28px;font-weight:800;color:var(--pri)">{len(CATS)}</div><div style="font-size:12px;color:var(--text-m)">{"健康分类" if is_zh else "Categories"}</div></div>
<div><div style="font-size:28px;font-weight:800;color:var(--pri)">{total_articles}</div><div style="font-size:12px;color:var(--text-m)">{"专业文章" if is_zh else "Articles"}</div></div>
<div><div style="font-size:28px;font-weight:800;color:var(--pri)">{len(AGE_GUIDES)}</div><div style="font-size:12px;color:var(--text-m)">{"年龄段指南" if is_zh else "Age Guides"}</div></div>
<div><div style="font-size:28px;font-weight:800;color:var(--pri)">2</div><div style="font-size:12px;color:var(--text-m)">{"语言版本" if is_zh else "Languages"}</div></div>
</div></div>'''

    # Categories section
    h += f'<div class="sec"><h2>{"健康知识分类" if is_zh else "Health Categories"}</h2><p class="sub">{"点击任一分类，探索详细的健康知识" if is_zh else "Click any category to explore detailed health information"}</p><div class="g3">'
    for cat_id, cat_en, cat_zh, emoji, color in CATS:
        cn = cat_zh if is_zh else cat_en
        articles = ALL_ARTICLES.get(cat_id, [])
        h += f'''<a href="{prefix}/{cat_id}/" class="card" style="text-decoration:none;border-left:4px solid {color}">
<div style="display:flex;align-items:center;gap:14px"><div class="cat-icon" style="background:{color}15">{emoji}</div>
<div><div style="font-weight:700;font-size:15px;color:var(--text)">{cn}</div>
<div style="font-size:12px;color:var(--text-m)">{len(articles)} {"篇文章" if is_zh else " articles"}</div></div></div></a>'''
    h += '</div></div>'

    # Age Guide section
    h += f'<div class="sec-a"><div class="sec"><h2>{"各年龄段健康指南" if is_zh else "Health Guide by Age"}</h2><p class="sub">{"不同年龄段有不同的健康重点" if is_zh else "Different ages have different health priorities"}</p><div class="g4">'
    for ag in AGE_GUIDES:
        an = ag['nz'] if is_zh else ag['n']
        ar = ag['rz'] if is_zh else ag['r']
        h += f'''<a href="{prefix}/age-guide/{ag['id']}.html" class="age-card" style="text-decoration:none">
<div class="age-emoji">{ag['emoji']}</div>
<div style="font-weight:700;color:var(--text)">{an}</div>
<div style="font-size:13px;color:var(--text-m)">{ar}</div></a>'''
    h += '</div></div></div>'

    # Featured articles from a few categories
    h += f'<div class="sec"><h2>{"热门健康话题" if is_zh else "Popular Health Topics"}</h2><p class="sub">{"最常搜索和阅读的健康知识" if is_zh else "Most searched and read health topics"}</p><div class="g2">'
    featured_cats = ["diseases","nutrition","mental","heart","sleep"]
    count = 0
    for fc in featured_cats:
        for art in ALL_ARTICLES.get(fc, [])[:2]:
            an = art['nz'] if is_zh else art['n']
            ad = (art['dz'] if is_zh else art['d'])[:100] + '...'
            cat = CAT_MAP[fc]
            h += f'''<a href="{prefix}/{fc}/{art['id']}.html" class="card" style="text-decoration:none">
<div style="display:flex;gap:14px;align-items:start"><div class="cat-icon" style="background:{cat[4]}15;min-width:48px;width:48px;height:48px;font-size:22px">{cat[3]}</div>
<div><div style="font-weight:700;color:var(--text);margin-bottom:4px">{e(an)}</div>
<div style="font-size:13px;color:var(--text-m);line-height:1.6">{e(ad)}</div></div></div></a>'''
            count += 1
            if count >= 8: break
        if count >= 8: break
    h += '</div></div>'

    h += footer(lang)
    h += '</body></html>'
    fp = f'zh/index.html' if is_zh else 'index.html'
    page(fp, h)

def gen_categories_page(lang):
    is_zh = lang == 'zh'
    p = f'{BASE}/zh' if is_zh else BASE
    path = f'{p}/categories/'
    title = "健康百科分类 - " + SITE_NAME_ZH if is_zh else "Health Categories - " + SITE_NAME
    desc = "浏览所有17个健康分类" if is_zh else "Browse all 17 health categories"

    bc = [(SITE_NAME_ZH if is_zh else "Home", f"{p}/"), ("健康百科" if is_zh else "Health A-Z", None)]
    h = head(title, desc, path, lang) + nav(lang)
    h += f'<div class="hero2"><h1>{"健康百科" if is_zh else "Health A-Z"}</h1><p>{"探索17个健康领域的专业知识" if is_zh else "Explore expert knowledge across 17 health domains"}</p></div>'
    h += f'<div class="sec">{breadcrumb_html(bc, lang)}<div class="g2">'
    for cat_id, cat_en, cat_zh, emoji, color in CATS:
        cn = cat_zh if is_zh else cat_en
        articles = ALL_ARTICLES.get(cat_id, [])
        sample = ', '.join([(a['nz'] if is_zh else a['n']) for a in articles[:3]])
        h += f'''<a href="{p}/{cat_id}/" class="card" style="text-decoration:none">
<div style="display:flex;align-items:center;gap:16px;margin-bottom:12px"><div class="cat-icon" style="background:{color}15;font-size:32px">{emoji}</div>
<div><div style="font-weight:700;font-size:17px;color:var(--text)">{cn}</div>
<div style="font-size:13px;color:var(--text-m)">{len(articles)} {"篇文章" if is_zh else " articles"}</div></div></div>
<div style="font-size:13px;color:var(--text-l)">{"包括：" if is_zh else "Includes: "}{e(sample)}...</div></a>'''
    h += '</div></div>'
    h += footer(lang) + '</body></html>'
    fp = f'zh/categories/index.html' if is_zh else 'categories/index.html'
    page(fp, h)

def gen_category_index(cat_id, articles, lang):
    is_zh = lang == 'zh'
    p = f'{BASE}/zh' if is_zh else BASE
    cat = CAT_MAP[cat_id]
    cn = cat[2] if is_zh else cat[1]
    path = f'{p}/{cat_id}/'
    title = f"{cn} - {SITE_NAME_ZH if is_zh else SITE_NAME}"
    desc = f"{'关于' if is_zh else 'Learn about '}{cn}{'的全面健康知识' if is_zh else ' - comprehensive health information'}"

    bc = [(SITE_NAME_ZH if is_zh else "Home", f"{p}/"), ("健康百科" if is_zh else "Health A-Z", f"{p}/categories/"), (cn, None)]
    h = head(title, desc, path, lang) + nav(lang)
    h += f'<div class="hero2" style="background:linear-gradient(135deg,{cat[4]}dd,{cat[4]}88)"><div style="font-size:56px;margin-bottom:12px">{cat[3]}</div><h1>{cn}</h1><p>{len(articles)} {"篇专业文章" if is_zh else " expert articles"}</p></div>'
    h += f'<div class="sec">{breadcrumb_html(bc, lang)}{breadcrumb_json(bc)}<div class="g2">'
    for art in articles:
        an = art['nz'] if is_zh else art['n']
        ad = (art['dz'] if is_zh else art['d'])[:120] + '...'
        h += f'''<a href="{p}/{cat_id}/{art['id']}.html" class="card" style="text-decoration:none">
<div style="font-weight:700;font-size:16px;color:var(--text);margin-bottom:8px">{e(an)}</div>
<div style="font-size:14px;color:var(--text-m);line-height:1.6">{e(ad)}</div>
<div style="margin-top:12px;font-size:13px;color:var(--pri);font-weight:600">{"阅读详情 →" if is_zh else "Read More →"}</div></a>'''
    h += '</div></div>'
    h += footer(lang) + '</body></html>'
    fp = f'zh/{cat_id}/index.html' if is_zh else f'{cat_id}/index.html'
    page(fp, h)

def gen_article_page(article, cat_id, lang):
    is_zh = lang == 'zh'
    p = f'{BASE}/zh' if is_zh else BASE
    cat = CAT_MAP[cat_id]
    cn = cat[2] if is_zh else cat[1]
    an = article['nz'] if is_zh else article['n']
    ad = article['dz'] if is_zh else article['d']
    path = f'{p}/{cat_id}/{article["id"]}.html'
    title = f"{an} - {cn} - {SITE_NAME_ZH if is_zh else SITE_NAME}"

    bc_items = [(SITE_NAME_ZH if is_zh else "Home", f"{p}/"), (cn, f"{p}/{cat_id}/"), (an, None)]
    h = head(title, ad[:160], path, lang) + nav(lang)

    # Article header
    h += f'''<div style="background:linear-gradient(135deg,{cat[4]}10,var(--bg));padding:40px 20px 20px">
<div class="article" style="max-width:800px;margin:0 auto">{breadcrumb_html(bc_items, lang)}{breadcrumb_json(bc_items)}
<div style="display:flex;align-items:center;gap:14px;margin-bottom:16px">
<div class="cat-icon" style="background:{cat[4]}20;font-size:28px">{cat[3]}</div>
<div><span class="badge" style="background:{cat[4]}15;color:{cat[4]}">{cn}</span></div></div>
<h1 style="margin-bottom:12px">{e(an)}</h1></div></div>'''

    # Article body
    h += '<div style="padding:32px 20px"><div class="article" style="max-width:800px;margin:0 auto"><div class="article-body">'

    # Description
    h += f'<h3>{"概述" if is_zh else "Overview"}</h3><p>{e(ad)}</p>'

    # Symptoms
    syms = article['symz'] if is_zh else article['sym']
    h += f'<div class="info-box info-sym"><h3>{"常见症状" if is_zh else "Common Symptoms"}</h3><ul>'
    for s in syms:
        if s.strip(): h += f'<li>{e(s.strip())}</li>'
    h += '</ul></div>'

    # Prevention
    prevs = article['prevz'] if is_zh else article['prev']
    h += f'<div class="info-box info-prev"><h3>{"预防措施" if is_zh else "Prevention"}</h3><ul>'
    for pr in prevs:
        if pr.strip(): h += f'<li>{e(pr.strip())}</li>'
    h += '</ul></div>'

    # Treatment
    treats = article['treatz'] if is_zh else article['treat']
    h += f'<div class="info-box info-treat"><h3>{"治疗方法" if is_zh else "Treatment Options"}</h3><ul>'
    for t in treats:
        if t.strip(): h += f'<li>{e(t.strip())}</li>'
    h += '</ul></div>'

    # When to see a doctor
    h += f'''<div class="info-box info-warn"><h3>{"何时就医" if is_zh else "When to See a Doctor"}</h3>
<p style="font-size:14px">{"如果您出现上述症状且持续不缓解，或症状严重影响日常生活，请及时就医。早期诊断和治疗对于改善预后至关重要。" if is_zh else "If you experience any of the symptoms listed above that persist or worsen, or if they significantly impact your daily life, seek medical attention promptly. Early diagnosis and treatment are crucial for better outcomes."}</p></div>'''

    # Related articles from same category
    all_in_cat = ALL_ARTICLES.get(cat_id, [])
    related = [a for a in all_in_cat if a['id'] != article['id']][:4]
    if related:
        h += f'<div class="related"><h3>{"相关文章" if is_zh else "Related Articles"}</h3><div class="g2" style="margin-top:16px">'
        for ra in related:
            rn = ra['nz'] if is_zh else ra['n']
            rd = (ra['dz'] if is_zh else ra['d'])[:80] + '...'
            h += f'''<a href="{p}/{cat_id}/{ra['id']}.html" class="card" style="text-decoration:none;padding:18px">
<div style="font-weight:600;color:var(--text);margin-bottom:4px;font-size:14px">{e(rn)}</div>
<div style="font-size:12px;color:var(--text-m)">{e(rd)}</div></a>'''
        h += '</div></div>'

    h += '</div></div></div>'

    # Schema.org
    schema = {"@context":"https://schema.org","@type":"MedicalWebPage","name":an,"description":ad[:160],"url":f"{DOMAIN}{path}","inLanguage":"zh-CN" if is_zh else "en","isPartOf":{"@type":"WebSite","name":SITE_NAME}}
    h += f'<script type="application/ld+json">{json.dumps(schema)}</script>'

    h += footer(lang) + '</body></html>'
    fp = f'zh/{cat_id}/{article["id"]}.html' if is_zh else f'{cat_id}/{article["id"]}.html'
    page(fp, h)

def gen_age_guide_index(lang):
    is_zh = lang == 'zh'
    p = f'{BASE}/zh' if is_zh else BASE
    path = f'{p}/age-guide/'
    title = "年龄健康指南 - " + SITE_NAME_ZH if is_zh else "Health Guide by Age - " + SITE_NAME
    desc = "各年龄段健康重点和建议" if is_zh else "Health priorities and recommendations for every age"

    bc = [(SITE_NAME_ZH if is_zh else "Home", f"{p}/"), ("年龄指南" if is_zh else "Age Guide", None)]
    h = head(title, desc, path, lang) + nav(lang)
    h += f'<div class="hero2"><div style="font-size:56px;margin-bottom:12px">👨‍👩‍👧‍👦</div><h1>{"各年龄段健康指南" if is_zh else "Health Guide by Age"}</h1><p>{"从婴儿到老年，每个阶段的健康要点" if is_zh else "Health essentials from infancy to golden years"}</p></div>'
    h += f'<div class="sec">{breadcrumb_html(bc, lang)}<div class="g3">'
    for ag in AGE_GUIDES:
        an = ag['nz'] if is_zh else ag['n']
        ar = ag['rz'] if is_zh else ag['r']
        ad = (ag['dz'] if is_zh else ag['d'])[:100] + '...'
        h += f'''<a href="{p}/age-guide/{ag['id']}.html" class="age-card" style="text-decoration:none">
<div class="age-emoji">{ag['emoji']}</div>
<div style="font-weight:700;color:var(--text);font-size:17px;margin-bottom:4px">{an}</div>
<div style="color:var(--pri);font-size:13px;font-weight:600;margin-bottom:8px">{ar}</div>
<div style="font-size:13px;color:var(--text-m)">{e(ad)}</div></a>'''
    h += '</div></div>'
    h += footer(lang) + '</body></html>'
    fp = f'zh/age-guide/index.html' if is_zh else 'age-guide/index.html'
    page(fp, h)

def gen_age_guide_page(guide, lang):
    is_zh = lang == 'zh'
    p = f'{BASE}/zh' if is_zh else BASE
    an = guide['nz'] if is_zh else guide['n']
    ar = guide['rz'] if is_zh else guide['r']
    ad = guide['dz'] if is_zh else guide['d']
    path = f'{p}/age-guide/{guide["id"]}.html'
    title = f"{an} ({ar}) - {SITE_NAME_ZH if is_zh else SITE_NAME}"

    bc = [(SITE_NAME_ZH if is_zh else "Home", f"{p}/"), ("年龄指南" if is_zh else "Age Guide", f"{p}/age-guide/"), (an, None)]
    h = head(title, ad[:160], path, lang) + nav(lang)
    h += f'<div class="hero2"><div style="font-size:64px;margin-bottom:12px">{guide["emoji"]}</div><h1>{an}</h1><p>{ar}</p></div>'
    h += f'<div style="padding:40px 20px"><div class="article" style="max-width:800px;margin:0 auto">{breadcrumb_html(bc, lang)}'
    h += f'<div class="article-body"><p style="font-size:17px;line-height:1.8">{e(ad)}</p>'

    # Key health priorities
    priorities = guide['priz'] if is_zh else guide['pri']
    h += f'<div class="info-box info-sym"><h3>{"健康重点" if is_zh else "Key Health Priorities"}</h3><ul>'
    for pr in priorities.split('|'):
        if pr.strip(): h += f'<li>{e(pr.strip())}</li>'
    h += '</ul></div>'

    # Screenings
    screens = guide['scrz'] if is_zh else guide['scr']
    h += f'<div class="info-box info-prev"><h3>{"推荐检查" if is_zh else "Recommended Screenings"}</h3><ul>'
    for sc in screens.split('|'):
        if sc.strip(): h += f'<li>{e(sc.strip())}</li>'
    h += '</ul></div>'

    # Nutrition tips
    nutri = guide['nutz'] if is_zh else guide['nut']
    h += f'<div class="info-box info-treat"><h3>{"营养建议" if is_zh else "Nutrition Tips"}</h3><ul>'
    for nt in nutri.split('|'):
        if nt.strip(): h += f'<li>{e(nt.strip())}</li>'
    h += '</ul></div>'

    # Exercise
    exercise = guide['exz'] if is_zh else guide['ex']
    h += f'<div class="info-box" style="background:#fff3e0;border-left:4px solid #ff8c00"><h3>{"运动建议" if is_zh else "Exercise Recommendations"}</h3><ul style="list-style:none;padding:0">'
    for ex in exercise.split('|'):
        if ex.strip(): h += f'<li style="padding:6px 0 6px 28px;position:relative;font-size:15px"><span style="position:absolute;left:4px;top:14px;width:8px;height:8px;border-radius:50%;background:#ff8c00"></span>{e(ex.strip())}</li>'
    h += '</ul></div>'

    h += '</div></div></div>'
    h += footer(lang) + '</body></html>'
    fp = f'zh/age-guide/{guide["id"]}.html' if is_zh else f'age-guide/{guide["id"]}.html'
    page(fp, h)

def gen_about(lang):
    is_zh = lang == 'zh'
    p = f'{BASE}/zh' if is_zh else BASE
    path = f'{p}/about.html'
    title = "关于我们 - " + SITE_NAME_ZH if is_zh else "About - " + SITE_NAME
    desc = "了解HealthPedia健康百科" if is_zh else "Learn about HealthPedia"

    bc = [(SITE_NAME_ZH if is_zh else "Home", f"{p}/"), ("关于" if is_zh else "About", None)]
    h = head(title, desc, path, lang) + nav(lang)
    h += f'<div class="hero2"><h1>{"关于 " + SITE_NAME_ZH if is_zh else "About " + SITE_NAME}</h1></div>'
    h += f'<div style="padding:40px 20px"><div style="max-width:700px;margin:0 auto">{breadcrumb_html(bc, lang)}'

    if is_zh:
        h += '''<div class="article-body">
<p>健康百科（HealthPedia）是一个免费的中英双语健康知识平台，旨在为公众提供准确、易懂、全面的健康信息。</p>
<h3>我们的使命</h3>
<p>我们相信健康知识应该对每个人都是免费和可获取的。本网站涵盖17个健康领域，从常见疾病到中医养生，从婴幼儿护理到老年健康，为不同年龄段的人群提供针对性的健康指导。</p>
<h3>内容声明</h3>
<p>本网站所有内容仅供健康教育和参考目的，不能替代专业医疗建议、诊断或治疗。如果您有任何健康问题，请务必咨询合格的医疗保健专业人员。</p>
<h3>双语服务</h3>
<p>我们提供完整的中英文双语内容，方便不同语言背景的用户获取健康信息。您可以随时通过页面右上角的语言切换按钮在中英文之间切换。</p>
</div>'''
    else:
        h += '''<div class="article-body">
<p>HealthPedia is a free bilingual (English/Chinese) health knowledge platform dedicated to providing accurate, accessible, and comprehensive health information to the public.</p>
<h3>Our Mission</h3>
<p>We believe health knowledge should be free and accessible to everyone. This website covers 17 health domains, from common diseases to traditional Chinese medicine, from infant care to senior health, providing targeted health guidance for people of all ages.</p>
<h3>Content Disclaimer</h3>
<p>All content on this website is for health education and reference purposes only and cannot substitute professional medical advice, diagnosis, or treatment. If you have any health concerns, please consult a qualified healthcare professional.</p>
<h3>Bilingual Service</h3>
<p>We provide complete bilingual content in English and Chinese, making health information accessible to users of different language backgrounds. You can switch between languages at any time using the toggle in the top-right corner.</p>
</div>'''

    h += '</div></div>'
    h += footer(lang) + '</body></html>'
    fp = f'zh/about.html' if is_zh else 'about.html'
    page(fp, h)

def gen_sitemap():
    urls = []
    for lang in ['en','zh']:
        p = f'{BASE}/zh' if lang=='zh' else BASE
        urls.append(f'{DOMAIN}{p}/')
        urls.append(f'{DOMAIN}{p}/categories/')
        urls.append(f'{DOMAIN}{p}/age-guide/')
        urls.append(f'{DOMAIN}{p}/about.html')
        for cat_id, arts in ALL_ARTICLES.items():
            urls.append(f'{DOMAIN}{p}/{cat_id}/')
            for a in arts:
                urls.append(f'{DOMAIN}{p}/{cat_id}/{a["id"]}.html')
        for ag in AGE_GUIDES:
            urls.append(f'{DOMAIN}{p}/age-guide/{ag["id"]}.html')

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        xml += f'  <url><loc>{u}</loc><changefreq>weekly</changefreq></url>\n'
    xml += '</urlset>'
    page('sitemap.xml', xml)

def gen_robots():
    page('robots.txt', f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}{BASE}/sitemap.xml\n')

# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    total = 0
    for lang in ['en','zh']:
        lname = 'Chinese' if lang=='zh' else 'English'
        print(f"\n📝 Generating {lname} pages...")

        gen_homepage(lang); total += 1
        gen_categories_page(lang); total += 1
        print(f"  ✓ Homepage & categories index")

        for cat_id, articles in ALL_ARTICLES.items():
            gen_category_index(cat_id, articles, lang); total += 1
            for art in articles:
                gen_article_page(art, cat_id, lang); total += 1
            print(f"  ✓ {CAT_MAP[cat_id][1]}: {len(articles)} articles")

        gen_age_guide_index(lang); total += 1
        for ag in AGE_GUIDES:
            gen_age_guide_page(ag, lang); total += 1
        print(f"  ✓ {len(AGE_GUIDES)} age guide pages")

        gen_about(lang); total += 1
        print(f"  ✓ About page")

    gen_sitemap(); total += 1
    gen_robots(); total += 1
    print(f"\n  ✓ Sitemap & robots.txt")

    file_count = sum(len(files) for _, _, files in os.walk(OUT))
    size = sum(os.path.getsize(os.path.join(d, f)) for d, _, files in os.walk(OUT) for f in files)

    print(f"\n{'='*50}")
    print(f"✅ HealthPedia site generated!")
    print(f"   Total HTML pages: {total}")
    print(f"   Total files: {file_count}")
    print(f"   Total size: {size/1024:.0f} KB")
    print(f"   Output: {OUT}/")
    print(f"{'='*50}")
