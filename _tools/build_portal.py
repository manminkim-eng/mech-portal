# -*- coding: utf-8 -*-
"""
MANMIN 기계설비 계산서 통합 포털 — index.html 생성기
  · 도구·근거 데이터는 아래 TOOLS / LAWS 한 곳에서만 관리한다.
  · 원칙(2026-10-29 MIN 승인): 포털에는 근거 조문·시행일만 싣고, 수치 기준은 각 계산서에 둔다.
  · 근거 확인: LawMCP(국가법령정보) 2026-10-29 조회. KDS 명칭은 「기계설비 기술기준」 별표 각 1.3(타 규정과의 관계) 표기.
사용: python build_portal.py  →  ../index.html
"""
import html, os, datetime

VER = "1.0.2"   # 1.0.2 (2026-10-30) 앱 설치 단추 · 아이폰 안내 · 하단 안내 띠 / 1.0.1 사용자 매뉴얼 Ver-1.0 연결
CHECKED = "2026-10-29"          # 근거 조문 대조일
BASE = "https://manminkim-eng.github.io"

GROUPS = [
    ("plumb", "위생·배수", "급수 · 배수 · 우수 · 급탕"),
    ("air",   "공조·환기", "냉온수 배관 · 덕트 · 환기"),
    ("heat",  "열원·반송", "펌프 · 냉난방 부하"),
]

# no, group, name, en, repo, ver, accent, desc(정성 서술 — 수치 기재 금지), basis(근거 칩)
TOOLS = [
    ("20", "plumb", "건물 우수관경", "Roof Drain", "Roof-Drain", "5.0.14", "#fbbf24",
     "건축물 옥상 배수의 우수 수직관·수평관 관경을 지역 강우 자료로 산정합니다.",
     ["KDS 31 30 35", "기상청 1시간 최다강수량"]),
    ("21", "plumb", "위생배관 관경", "Sanitary Piping", "Sanitary-Piping-System", "5.0.12", "#38bdf8",
     "헌터 곡선과 하젠-윌리엄스 공식으로 급수·배수 관경을 산정합니다.",
     ["KDS 31 30 15", "KDS 31 30 25", "기술기준 별표 5 · 6 · 8", "IPC 2021 부록 E"]),
    ("25", "plumb", "급탕량 · 보일러", "Hot Water Supply", "Hot-Water-Supply-System", "5.0.2", "#fb923c",
     "건물 용도별 급탕량과 급탕 보일러 출력을 산정합니다.",
     ["KDS 31 30 20", "기술기준 별표 5"]),
    ("22", "air", "냉온수 배관", "Chilled · Hot Water Piping", "CHWS-STSTEM", "5.0.13", "#22d3ee",
     "냉·온수 순환배관의 관경과 유속·마찰손실을 산정합니다.",
     ["KDS 31 25 25", "기술기준 별표 8"]),
    ("23", "air", "공조 덕트", "Air Duct", "Air-Conditioning-Duct", "5.1.2", "#5a9ae8",
     "공조·환기 덕트의 풍량별 규격을 산정합니다.",
     ["KDS 31 25 30", "기술기준 별표 9"]),
    ("26", "air", "기계환기설비", "Mechanical Ventilation", "ventilation-equipment", "5.0.11", "#a78bfa",
     "용도·면적·재실 인원으로 필요 환기량을 산정합니다.",
     ["설비규칙 제11조 · 별표 1의6", "기술기준 별표 3"]),
    ("24", "heat", "설비 펌프", "Booster Pump", "Booster-Pump", "5.0.3", "#60a5fa",
     "전양정과 축동력을 계산해 펌프 용량을 선정합니다.",
     ["기술기준 별표 1 · 5 · 6", "에너지절약설계기준 제8조", "KS B 6318"]),
    ("27", "heat", "냉난방 부하계산", "RTS Load Calculation", "Radiant-Time-Series-Method", "5.3.2", "#2dd4bf",
     "RTS(복사시계열)법으로 냉방 피크 부하와 난방 부하를 계산합니다.",
     ["ASHRAE RTS법", "에너지절약설계기준 별표 1 · 7"]),
]

# 이름, 구분, 현행(번호 · 시행일), 관련 조문, 적용 도구 번호
LAWS = [
    ("건축물의 설비기준 등에 관한 규칙", "국토교통부령",
     "2026-08-24 시행", "제11조(공동주택 및 다중이용시설의 환기설비기준 등) · 별표 1의6", "26"),
    ("기계설비 기술기준", "국토교통부 고시",
     "제2026-360호 · 2026-07-08 시행", "제8조 · 별표 1 · 3 · 5 · 6 · 8 · 9", "21 · 22 · 23 · 24 · 25 · 26"),
    ("건축물의 에너지절약설계기준", "국토교통부 고시",
     "제2026-360호 · 2026-07-08 시행", "제8조(설계용 외기조건 · 펌프 효율) · 별표 1 · 별표 7", "24 · 27"),
    ("KDS 31 설비 설계기준", "국가건설기준(KCSC)",
     "국가건설기준센터 현행본", "31 25 25 배관설비 · 31 25 30 덕트설비 · 31 30 15 급수설비 · 31 30 20 급탕설비 · 31 30 25 배수통기설비 · 31 30 35 우수설비", "20 · 21 · 22 · 23 · 25"),
    ("참고 기준", "국외 · 기상자료",
     "각 계산서 표기 판", "ASHRAE Handbook—Fundamentals(RTS법) · IPC 2021 부록 E · KS B 6318 · 기상청 1시간 최다강수량", "20 · 21 · 24 · 27"),
]

e = html.escape

def card(t):
    no, g, name, en, repo, ver, acc, desc, basis = t
    chips = "".join(f'<span class="chip">{e(b)}</span>' for b in basis)
    return f'''
    <a class="tcard" data-g="{g}" href="../{repo}/" style="--acc:{acc}" aria-label="{e(name)} 계산서 열기">
      <div class="tc-top"><span class="tc-dot" aria-hidden="true"></span><span class="tc-no">M · {no}</span><span class="tc-ver">Ver {ver}</span></div>
      <h3 class="tc-name">{e(name)}</h3>
      <div class="tc-en">{e(en)}</div>
      <p class="tc-desc">{e(desc)}</p>
      <div class="tc-chips" aria-label="근거 기준">{chips}</div>
      <div class="tc-foot">
        <span class="tc-man" role="link" tabindex="0" data-href="../{repo}/manual/">사용자 매뉴얼</span>
        <span class="tc-go">계산서 열기 <span class="arw" aria-hidden="true">→</span></span>
      </div>
    </a>'''

def group(gid, gname, gsub):
    items = [t for t in TOOLS if t[1] == gid]
    return f'''
  <section class="grp" id="g-{gid}" data-g="{gid}">
    <div class="grp-hd"><span class="grp-tag">{e(gname)}</span><span class="grp-sub">{e(gsub)}</span><span class="grp-n">{len(items)} tools</span></div>
    <div class="grid">{"".join(card(t) for t in items)}
    </div>
  </section>'''

law_rows = "".join(f'''
        <tr><th scope="row">{e(n)}</th><td>{e(k)}</td><td class="num">{e(d)}</td><td>{e(a)}</td><td class="num">{e(t)}</td></tr>''' for n, k, d, a, t in LAWS)

tabs = f'<button class="tab on" data-tab="all" role="tab" aria-selected="true">전체 <span class="tn">{len(TOOLS)}</span></button>' + "".join(
    f'<button class="tab" data-tab="{g}" role="tab" aria-selected="false">{e(n)} <span class="tn">{sum(1 for t in TOOLS if t[1]==g)}</span></button>' for g, n, _ in GROUPS)

page = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ENGINEER KIM MANMIN · 기계설비 계산서 통합 포털</title>
<meta name="description" content="기계설비 계산서 통합 포털 — 위생·배수 · 공조·환기 · 열원·반송 8종 계산서와 근거 법령·기준 안내 | Engineer Kim Manmin">
<meta name="theme-color" content="#0b1626">
<meta name="color-scheme" content="dark">
<link rel="manifest" href="manifest.json">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="기계설비 포털">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="./assets/fonts/manmin-fonts.css"><!-- 로컬 폴백 폰트 -->
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg:#0b1220;--bg-card:#121c30;--bg-deep:#080d18;
  --line:#1e2e50;--line2:#2a4070;
  --t-high:#f2f5ff;--t-body:#c2d0ec;--t-sub:#8aa2c8;
  --mech:#5a9ae8;--mech-lt:#9cc3f5;--gold:#d8ac50;--gold-lt:#f1cd7c;
  --f-kr:'Noto Sans KR','Noto Sans KR Local','Apple SD Gothic Neo','Malgun Gothic',sans-serif;
  --f-mono:'JetBrains Mono','Noto Sans KR','Noto Sans KR Local',Consolas,monospace;
  --radius:12px;--shadow:0 4px 20px rgba(0,0,0,.35);
}}
html{{scroll-behavior:smooth;-webkit-text-size-adjust:100%}}
body{{font-family:var(--f-kr);background:var(--bg);color:var(--t-body);line-height:1.7;-webkit-font-smoothing:antialiased;overflow-x:hidden;min-height:100vh}}
.bg{{position:fixed;inset:0;z-index:0;pointer-events:none;
  background-image:linear-gradient(rgba(90,154,232,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(90,154,232,.04) 1px,transparent 1px),
  radial-gradient(ellipse 90% 50% at 50% -10%,rgba(45,81,134,.35),transparent 65%);background-size:40px 40px,40px 40px,100% 100%}}
.wrap{{position:relative;z-index:1;max-width:1120px;margin:0 auto;padding:0 24px 80px}}
a{{color:inherit}}
:focus-visible{{outline:2px solid var(--gold);outline-offset:3px}}

/* HEADER */
.hd{{padding:52px 0 8px;text-align:center}}
.pill{{display:inline-flex;align-items:center;gap:8px;padding:6px 14px;border:1px solid var(--line2);border-radius:999px;font-size:.8rem;color:var(--mech-lt);background:rgba(90,154,232,.06)}}
.pill i{{width:7px;height:7px;border-radius:50%;background:#4ade80;box-shadow:0 0 0 3px rgba(74,222,128,.18)}}
.brand{{display:flex;align-items:center;justify-content:center;gap:18px;margin:22px 0 14px;flex-wrap:wrap}}
.brand img{{width:72px;height:72px;border-radius:14px;border:1px solid var(--line2)}}
.brand-t{{text-align:left}}
.brand-e{{font-family:var(--f-mono);font-size:.8rem;letter-spacing:.3em;color:var(--mech-lt);text-transform:uppercase}}
.brand-n{{font-family:var(--f-mono);font-weight:700;font-size:2rem;letter-spacing:.06em;color:var(--t-high);line-height:1.1}}
.ttl{{font-size:clamp(1.6rem,3.6vw,2.4rem);font-weight:900;letter-spacing:-.03em;color:var(--t-high);line-height:1.25}}
.ttl b{{color:var(--mech-lt);font-weight:900}}
.lead{{margin:12px auto 0;max-width:640px;font-size:1rem;color:var(--t-body)}}
.hline{{width:120px;height:2px;margin:26px auto 0;background:linear-gradient(90deg,transparent,var(--mech),transparent)}}

/* STATS */
.stats{{display:grid;grid-template-columns:repeat(5,1fr);gap:1px;margin:30px 0 26px;background:var(--line);border:1px solid var(--line);border-radius:var(--radius);overflow:hidden}}
.st{{background:var(--bg-card);padding:16px 12px;text-align:center}}
.st-n{{font-family:var(--f-mono);font-weight:700;font-size:1.35rem;color:var(--t-high)}}
.st-l{{font-size:.8rem;color:var(--t-sub)}}

/* TABS */
.tabs{{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-bottom:30px}}
.tab{{font:500 .92rem var(--f-kr);color:var(--t-sub);background:var(--bg-card);border:1px solid var(--line2);border-radius:999px;min-height:44px;padding:0 18px;cursor:pointer;display:inline-flex;align-items:center;gap:8px;transition:.2s}}
.tab:hover{{color:var(--t-high);border-color:var(--mech)}}
.tab.on{{color:#0b1220;background:var(--mech-lt);border-color:var(--mech-lt);font-weight:700}}
.tn{{font-family:var(--f-mono);font-size:.78rem;opacity:.8}}
.tab-law{{text-decoration:none}}
.tab-man{{border-color:var(--gold);color:var(--gold-lt)}}.tab-man:hover{{border-color:var(--gold-lt);color:var(--t-high)}}

/* GROUP */
.grp{{margin-bottom:40px}}
.grp-hd{{display:flex;align-items:center;gap:12px;margin-bottom:16px;flex-wrap:wrap}}
.grp-tag{{font-weight:700;color:var(--t-high);font-size:1.08rem;padding-left:12px;border-left:3px solid var(--mech)}}
.grp-sub{{font-size:.88rem;color:var(--t-sub)}}
.grp-n{{margin-left:auto;font-family:var(--f-mono);font-size:.78rem;color:var(--t-sub)}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}

/* CARD */
.tcard{{position:relative;display:flex;flex-direction:column;background:var(--bg-card);border:1px solid var(--line);border-radius:var(--radius);padding:22px 22px 18px;text-decoration:none;box-shadow:var(--shadow);transition:transform .22s,border-color .22s,box-shadow .22s;overflow:hidden}}
.tcard::before{{content:"";position:absolute;left:0;right:0;top:0;height:3px;background:linear-gradient(90deg,var(--acc),transparent);opacity:.85}}
.tcard:hover{{transform:translateY(-4px);border-color:var(--acc);box-shadow:0 12px 32px rgba(0,0,0,.45)}}
.tc-top{{display:flex;align-items:center;gap:8px;margin-bottom:12px}}
.tc-dot{{width:9px;height:9px;border-radius:50%;background:var(--acc)}}
.tc-no{{font-family:var(--f-mono);font-size:.78rem;letter-spacing:.08em;color:var(--t-sub)}}
.tc-ver{{margin-left:auto;font-family:var(--f-mono);font-size:.76rem;color:var(--t-sub);border:1px solid var(--line2);border-radius:6px;padding:1px 7px}}
.tc-name{{font-size:1.16rem;font-weight:700;letter-spacing:-.01em;color:var(--t-high);line-height:1.35}}
.tc-en{{font-family:var(--f-mono);font-size:.76rem;letter-spacing:.06em;color:var(--t-sub);text-transform:uppercase;margin-top:2px}}
.tc-desc{{margin:12px 0 14px;font-size:.92rem;line-height:1.7;flex:1}}
.tc-chips{{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:16px}}
.chip{{font-size:.78rem;color:var(--t-body);background:var(--bg-deep);border:1px solid var(--line2);border-radius:6px;padding:3px 8px}}
.tc-foot{{display:flex;align-items:center;gap:10px;border-top:1px solid var(--line);padding-top:12px}}
.tc-man{{font-size:.86rem;color:var(--mech-lt);min-height:44px;display:inline-flex;align-items:center;cursor:pointer;text-decoration:underline;text-underline-offset:3px}}
.tc-man:hover{{color:var(--gold-lt)}}
.tc-go{{margin-left:auto;font-size:.88rem;font-weight:700;color:var(--t-high)}}
.arw{{display:inline-block;transition:transform .22s}}
.tcard:hover .arw{{transform:translateX(4px)}}
.grp.off{{display:none}}

/* LAW */
.law{{margin-top:12px;scroll-margin-top:20px}}
.law-hd{{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin-bottom:12px}}
.law-hd h2{{font-size:1.3rem;font-weight:800;color:var(--t-high);letter-spacing:-.02em}}
.law-hd span{{font-size:.86rem;color:var(--t-sub)}}
.tbl-wrap{{overflow-x:auto;border:1px solid var(--line);border-radius:var(--radius);background:var(--bg-card)}}
table{{width:100%;border-collapse:collapse;font-size:.9rem;min-width:760px}}
th,td{{padding:12px 14px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}
thead th{{background:var(--bg-deep);color:var(--t-sub);font-weight:500;font-size:.82rem;white-space:nowrap}}
tbody th{{color:var(--t-high);font-weight:700}}
tbody tr:last-child th,tbody tr:last-child td{{border-bottom:0}}
td.num{{font-family:var(--f-mono);font-size:.84rem;white-space:nowrap}}
.note{{margin-top:14px;padding:14px 16px;border:1px solid var(--line2);border-left:3px solid var(--gold);border-radius:var(--radius);background:rgba(216,172,80,.05);font-size:.88rem}}
.note b{{color:var(--gold-lt)}}
.note a{{color:var(--mech-lt)}}

/* FOOTER */
.ft{{margin-top:48px;padding-top:22px;border-top:1px solid var(--line);display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font-size:.84rem;color:var(--t-sub)}}
.ft a{{color:var(--mech-lt)}}
.ft .mono{{font-family:var(--f-mono)}}

/* 앱 설치 (v1.0.2) */
.tab-inst{{font-weight:700}}
.tab-inst svg{{width:15px;height:15px;flex-shrink:0}}
.pwa-bar{{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:40;width:min(560px,calc(100% - 32px));display:flex;align-items:center;gap:12px;
  padding:12px 14px;background:var(--bg-card);border:1px solid var(--line2);border-left:3px solid var(--gold);border-radius:var(--radius);box-shadow:0 12px 32px rgba(0,0,0,.5)}}
.pwa-bar img{{width:40px;height:40px;border-radius:8px;flex-shrink:0}}
.pwa-bar-t{{flex:1;min-width:0;font-size:.88rem;line-height:1.5}}
.pwa-bar-t b{{display:block;color:var(--t-high);font-size:.95rem}}
.pwa-bar button,.ios-x,.ios-ok{{font:600 .88rem var(--f-kr);min-height:44px;padding:0 14px;border-radius:8px;cursor:pointer}}
.pwa-yes,.ios-ok{{background:var(--gold);color:#0b1220;border:0}}
.pwa-yes:hover,.ios-ok:hover{{background:var(--gold-lt)}}
.pwa-no,.ios-x{{background:transparent;color:var(--t-sub);border:1px solid var(--line2)}}
.pwa-no:hover,.ios-x:hover{{color:var(--t-high);border-color:var(--mech)}}
.ios-guide{{position:fixed;inset:0;z-index:50;display:flex;align-items:center;justify-content:center;padding:16px;background:rgba(5,9,18,.72)}}
.ios-box{{width:min(440px,100%);background:var(--bg-card);border:1px solid var(--line2);border-radius:var(--radius);box-shadow:0 16px 48px rgba(0,0,0,.6);padding:22px 22px 18px}}
.ios-box h2{{font-size:1.12rem;font-weight:800;color:var(--t-high);margin-bottom:12px}}
.ios-box ol{{list-style:none;counter-reset:s;display:grid;gap:10px;margin-bottom:12px}}
.ios-box li{{counter-increment:s;display:flex;gap:10px;align-items:flex-start;font-size:.92rem}}
.ios-box li::before{{content:counter(s);flex-shrink:0;width:24px;height:24px;border-radius:50%;background:var(--mech);color:#0b1220;font:700 .8rem var(--f-mono);display:flex;align-items:center;justify-content:center;margin-top:1px}}
.ios-box li svg{{width:16px;height:16px;vertical-align:-3px;color:var(--mech-lt)}}
.ios-note{{font-size:.82rem;color:var(--t-sub);border-top:1px solid var(--line);padding-top:10px;margin-bottom:14px}}
.ios-act{{display:flex;gap:8px;justify-content:flex-end}}
[hidden]{{display:none!important}}

/* 5단계 반응형 */
@media (max-width:1240px){{.wrap{{max-width:100%}}}}
@media (max-width:1024px){{.grid{{grid-template-columns:repeat(2,1fr)}}}}
@media (max-width:760px){{.stats{{grid-template-columns:repeat(3,1fr)}}.st:nth-child(n+4){{grid-column:span 1}}}}
@media (max-width:640px){{
  .wrap{{padding:0 16px 64px}}.hd{{padding-top:36px}}
  .grid{{grid-template-columns:1fr}}
  .stats{{grid-template-columns:repeat(2,1fr)}}.st:last-child{{grid-column:1/-1}}
  .brand img{{width:56px;height:56px}}.brand-n{{font-size:1.6rem}}
  .tab{{min-height:48px}}.tc-man{{min-height:48px}}
  .grp-n{{margin-left:0;width:100%}}
  .ft a{{display:inline-flex;align-items:center;min-height:48px}}
  .pwa-bar{{bottom:12px;flex-wrap:wrap}}.pwa-bar img{{display:none}}.pwa-bar-t{{flex-basis:100%}}
  .pwa-bar button,.ios-x,.ios-ok{{min-height:48px;flex:1}}
}}
@media (max-width:480px){{.brand-e{{letter-spacing:.2em}}.tabs{{justify-content:flex-start}}}}
@media (max-width:400px){{.tcard{{padding:18px 16px 14px}}}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important;scroll-behavior:auto!important}}}}
@media print{{.bg,.tabs,.pwa-bar,.ios-guide{{display:none!important}}body{{background:#fff;color:#111}}.tcard,.tbl-wrap,.st{{background:#fff;box-shadow:none;break-inside:avoid}}
  .tc-name,.ttl,.law-hd h2,tbody th,.st-n,.brand-n{{color:#111}}.grp.off{{display:block}}}}
</style>
</head>
<body>
<div class="bg" aria-hidden="true"></div>
<div class="wrap">

<header class="hd">
  <div class="pill"><i aria-hidden="true"></i>근거 조문 대조 {CHECKED} · 기계설비 기술기준 제2026-360호</div>
  <div class="brand">
    <img src="icons/icon-192.png" alt="ENGINEER KIM MANMIN 로고" width="72" height="72">
    <div class="brand-t"><div class="brand-e">Engineer</div><div class="brand-n">KIM MANMIN</div></div>
  </div>
  <h1 class="ttl">기계설비 <b>계산서 통합 포털</b></h1>
  <p class="lead">위생·배수 · 공조·환기 · 열원·반송 계산서 {len(TOOLS)}종을 한곳에서 열고, 계산서마다 적용한 근거 법령과 설계기준을 확인합니다.</p>
  <div class="hline" aria-hidden="true"></div>
</header>

<div class="stats">
  <div class="st"><div class="st-n">{len(TOOLS)}</div><div class="st-l">계산서(위생 3 · 공조 3 · 열원 2)</div></div>
  <div class="st"><div class="st-n">KDS 31</div><div class="st-l">설비 설계기준</div></div>
  <div class="st"><div class="st-n">고시</div><div class="st-l">기계설비 기술기준</div></div>
  <div class="st"><div class="st-n">PWA</div><div class="st-l">오프라인 지원</div></div>
  <div class="st"><div class="st-n">A4</div><div class="st-l">계산서 인쇄</div></div>
</div>

<nav class="tabs" role="tablist" aria-label="분류">
  {tabs}
  <a class="tab tab-law" href="#law">근거 법령·기준</a>
  <a class="tab tab-law tab-man" href="./manual/" target="_blank" rel="noopener" aria-label="포털 사용자 매뉴얼 (새 창)">사용자 매뉴얼</a>
  <button class="tab tab-man tab-inst" id="pwa-inst" type="button" hidden aria-label="이 포털을 앱으로 설치"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12"/><path d="M7 10l5 5 5-5"/><path d="M5 21h14"/></svg>앱 설치</button>
</nav>
{"".join(group(*g) for g in GROUPS)}

<section class="law" id="law">
  <div class="law-hd"><h2>근거 법령 · 설계기준</h2><span>대조일 {CHECKED} · 국가법령정보 기준</span></div>
  <div class="tbl-wrap">
    <table>
      <thead><tr><th scope="col">법령 · 기준</th><th scope="col">구분</th><th scope="col">현행</th><th scope="col">관련 조문 · 코드</th><th scope="col">적용 도구</th></tr></thead>
      <tbody>{law_rows}
      </tbody>
    </table>
  </div>
  <p class="note"><b>안내</b> — 이 포털은 계산서별 근거와 시행일만 안내합니다. 수치 기준(관경 · 풍량 · 환기량 등)은 각 계산서의 산출근거표에서 확인하십시오. 기계설비 기술기준과 에너지절약설계기준의 제2026-360호는 정부조직 개편에 따른 타법개정이며, 원 고시는 기계설비 기술기준 제2021-851호입니다. KDS 코드 원문과 개정 이력은 <a href="https://www.kcsc.re.kr/" target="_blank" rel="noopener">국가건설기준센터</a>에서 확인하십시오.</p>
</section>

<footer class="ft">
  <span>© 2026 김만민 건축사 · (주)대성건축사사무소 — <a href="{BASE}/KIMMANMIN/" target="_blank" rel="noopener">MANMIN 홈페이지</a></span>
  <span class="mono">MECH PORTAL · Ver {VER}</span>
</footer>
</div>

<div class="pwa-bar" id="pwa-bar" role="region" aria-label="앱 설치 안내" hidden>
  <img src="icons/icon-96.png" alt="" width="40" height="40">
  <div class="pwa-bar-t"><b>기계설비 포털을 앱으로 설치</b>홈 화면에서 바로 열고, 오프라인에서도 포털을 볼 수 있습니다.</div>
  <button class="pwa-no" id="pwa-no" type="button">닫기</button>
  <button class="pwa-yes" id="pwa-yes" type="button">설치</button>
</div>

<div class="ios-guide" id="ios-guide" role="dialog" aria-modal="true" aria-labelledby="ios-t" hidden>
  <div class="ios-box">
    <h2 id="ios-t">아이폰 · 아이패드에서 설치</h2>
    <ol>
      <li><span>화면 아래(아이패드는 위)의 <b>공유</b> 단추 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 15V3"/><path d="M7 8l5-5 5 5"/><path d="M5 12v8h14v-8"/></svg>를 누릅니다.</span></li>
      <li><span>목록에서 <b>홈 화면에 추가</b>를 고른 뒤 <b>추가</b>를 누릅니다.</span></li>
    </ol>
    <p class="ios-note">설치되는 범위는 이 포털입니다. 카드에서 연 계산서는 앱 안의 브라우저 창으로 열리며, 계산서도 앱으로 쓰려면 각 계산서 화면에서 같은 방법으로 설치합니다.</p>
    <div class="ios-act"><button class="ios-ok" id="ios-ok" type="button">확인</button></div>
  </div>
</div>

<script>
(function(){{
  var tabs=document.querySelectorAll('.tab[data-tab]'),grps=document.querySelectorAll('.grp');
  tabs.forEach(function(t){{t.addEventListener('click',function(){{
    var k=t.getAttribute('data-tab');
    tabs.forEach(function(x){{var on=x===t;x.classList.toggle('on',on);x.setAttribute('aria-selected',on?'true':'false');}});
    grps.forEach(function(g){{g.classList.toggle('off',k!=='all'&&g.getAttribute('data-g')!==k);}});
  }});}});
  function go(el,ev){{ev.preventDefault();ev.stopPropagation();window.open(el.getAttribute('data-href'),'_blank','noopener');}}
  document.querySelectorAll('.tc-man').forEach(function(m){{
    m.addEventListener('click',function(ev){{go(m,ev);}});
    m.addEventListener('keydown',function(ev){{if(ev.key==='Enter'||ev.key===' ')go(m,ev);}});
  }});
  if('serviceWorker' in navigator){{window.addEventListener('load',function(){{navigator.serviceWorker.register('./sw.js').catch(function(){{}});}});}}

  /* 앱 설치 (v1.0.2) — 지원 브라우저: beforeinstallprompt · 아이폰/아이패드: 안내 상자 · 설치된 앱 화면: 숨김 */
  var inst=document.getElementById('pwa-inst'),bar=document.getElementById('pwa-bar'),
      yes=document.getElementById('pwa-yes'),no=document.getElementById('pwa-no'),
      ios=document.getElementById('ios-guide'),iosOk=document.getElementById('ios-ok'),dp=null,last=null;
  var standalone=(window.matchMedia&&matchMedia('(display-mode: standalone)').matches)||navigator.standalone===true;
  var isIOS=/iPad|iPhone|iPod/.test(navigator.userAgent)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);
  function ss(k,v){{try{{if(v===undefined)return sessionStorage.getItem(k);sessionStorage.setItem(k,v);}}catch(e){{return null;}}}}
  function showBar(){{if(standalone||ss('mp-inst-bar'))return;setTimeout(function(){{if(!standalone&&(dp||isIOS))bar.hidden=false;}},2000);}}
  function hideAll(){{inst.hidden=true;bar.hidden=true;}}
  function openIOS(){{last=document.activeElement;bar.hidden=true;ios.hidden=false;iosOk.focus();}}
  function closeIOS(){{ios.hidden=true;if(last&&last.focus)last.focus();}}
  function doInstall(){{
    if(dp){{bar.hidden=true;dp.prompt();dp.userChoice.then(function(c){{if(c.outcome==='accepted')hideAll();dp=null;if(c.outcome!=='accepted')inst.hidden=true;}});}}
    else if(isIOS){{openIOS();}}
  }}
  if(!standalone){{
    window.addEventListener('beforeinstallprompt',function(e){{e.preventDefault();dp=e;inst.hidden=false;showBar();}});
    if(isIOS){{inst.hidden=false;showBar();}}
  }}
  window.addEventListener('appinstalled',function(){{dp=null;hideAll();}});
  inst.addEventListener('click',doInstall);yes.addEventListener('click',doInstall);
  no.addEventListener('click',function(){{bar.hidden=true;ss('mp-inst-bar','1');}});
  iosOk.addEventListener('click',closeIOS);
  ios.addEventListener('click',function(e){{if(e.target===ios)closeIOS();}});
  document.addEventListener('keydown',function(e){{if(e.key==='Escape'&&!ios.hidden)closeIOS();}});
}})();
</script>
</body>
</html>
'''
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "index.html")
open(out, "w", encoding="utf-8").write(page)
print("written", os.path.getsize(out), "bytes ·", len(TOOLS), "tools ·", len(LAWS), "laws")
