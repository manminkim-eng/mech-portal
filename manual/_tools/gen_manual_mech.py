# -*- coding: utf-8 -*-
"""기계설비 계산서 통합 포털 사용자 매뉴얼 생성기 (MANMIN 매뉴얼 공통 엔진 v-mh1 · 안내형 도구 — 계산 예제 없음)
   실행: MANUAL_DIR=<manual 폴더> python gen_manual_mech.py  →  <manual>/index.html
   도구·근거 데이터는 ../../_tools/build_portal.py 의 TOOLS · GROUPS · LAWS 를 그대로 읽는다(단일 원천).
   근거(LawMCP 대조 2026-10-29): 건축물의 설비기준 등에 관한 규칙(2026-08-24 시행) · 기계설비 기술기준 국토교통부고시 제2026-360호
   (2026-07-08 시행, 타법개정 · 원 고시 제2021-851호) · 건축물의 에너지절약설계기준 제2026-360호(2026-07-08 시행)"""
import os, sys, io, runpy, contextlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from manual_engine import fig, T, render, B, MARKS

with contextlib.redirect_stdout(io.StringIO()):
    D = runpy.run_path(os.path.join(HERE, '..', '..', '_tools', 'build_portal.py'))
TOOLS, GROUPS, LAWS, APPVER, CHECKED = D['TOOLS'], D['GROUPS'], D['LAWS'], D['VER'], D['CHECKED']

VER, DATE = 'Ver-1.0', '2026-10-30'
PDF = '기계설비통합포털_사용자매뉴얼_Ver-1.0.pdf'
APP_URL = 'https://manminkim-eng.github.io/mech-portal/'
APP = '기계설비 계산서 통합 포털'
G = 'https://manminkim-eng.github.io/'
def F(sid, cap, legend=None, **kw):
    if legend is None:
        legend = [k['label'] for k in MARKS.get(sid, {}).get('marks', [])] or None
    return fig(sid, cap, legend, **kw)
K = lambda t: '<div class="k1">' + t + '</div>'
BR = lambda t: '<div class="brk">' + t + '</div>'
EXTRA_CSS = """<style>
#fig-s07_card{max-width:420px}
.k1 td:first-child,.k1 th:first-child{white-space:nowrap}
.tri{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;align-items:start}
@media (max-width:760px){.tri{grid-template-columns:1fr}}
@media print{
  figure.shot{max-width:none!important}
  figure.shot .frame{width:fit-content;max-width:100%}
  figure.shot img{width:auto;height:auto;max-width:100%;max-height:118mm}
  figure.narrow img{max-height:105mm}
  .tri{grid-template-columns:repeat(3,1fr)}
  .brk .tbl{break-inside:auto}.brk tr{break-inside:avoid}.brk thead{display:table-header-group}
}
</style>"""
GNAME = {g: n for g, n, _ in GROUPS}
tool_rows = [[GNAME[t[1]], t[0], f'<a href="{G}{t[4]}/" target="_blank" rel="noopener">{t[2]}</a>', 'Ver ' + t[5], ' · '.join(t[8]),
              f'<a href="{G}{t[4]}/manual/" target="_blank" rel="noopener">매뉴얼</a>'] for t in TOOLS]
law_rows = [[n, k, d, a, t] for n, k, d, a, t in LAWS]
TOC = [
 ('ch0', '0. 이 매뉴얼에 대하여', []),
 ('ch1', '1. 한눈에 보기', [('s1-1', '화면 구성'), ('s1-2', '연결 계산서 8종')]),
 ('ch2', '2. 1분 따라하기', []),
 ('ch3', '3. 화면별 기능', [('s3-1', '머리'), ('s3-2', '분류 탭'), ('s3-3', '계산서 카드'), ('s3-4', '위생·배수'), ('s3-5', '공조·환기'), ('s3-6', '열원·반송'), ('s3-7', '근거 법령·설계기준'), ('s3-8', '휴대전화 화면')]),
 ('ch4', '4. 근거 해설', [('s4-1', '근거 체계'), ('s4-2', '고시 번호 읽는 법'), ('s4-3', '포털과 계산서의 역할')]),
 ('ch5', '5. 문제 해결·FAQ', []),
 ('ch6', '부록', [('a1', '버전 변경 내역'), ('a2', '용어')]),
]
S_ = []
S_.append(f"""{EXTRA_CSS}<section class="ch" id="ch0"><h2><span class="n">00</span>이 매뉴얼에 대하여</h2>
<p class="lead">{APP}은 건물 우수 · 위생배관 · 급탕 · 냉온수 배관 · 공조 덕트 · 기계환기 · 설비 펌프 · 냉난방 부하계산까지 <b>MANMIN 기계설비 계산서 8종의 진입 화면</b>입니다. 포털은 계산하지 않습니다. 카드를 눌러 계산서로 들어가고, 계산서마다 적용한 근거 법령과 설계기준을 한 화면에서 확인합니다.</p>
{K(T([
 ['대상 프로그램', f'{APP} <b>Ver {APPVER}</b>'],
 ['접속 주소', f'<a href="{APP_URL}" target="_blank" rel="noopener">manminkim-eng.github.io/mech-portal</a>'],
 ['매뉴얼 판', f'<b>{VER}</b> (초판) · {DATE} · 작성 김만민 건축사(㈜대성건축사사무소)'],
 ['내려받기', f'<a href="{PDF}" download>PDF(A4)</a> · <a href="../index.html">포털 열기</a>'],
 ['근거 대조', f'국가법령정보(LawMCP) {CHECKED} — 건축물의 설비기준 등에 관한 규칙 · 기계설비 기술기준 · 건축물의 에너지절약설계기준'],
 ['범위', '안내 · 연결 도구 — 수치 기준과 계산은 각 계산서에서 합니다'],
], ['항목', '내용']))}
<div class="note"><b>표기</b>그림 위 주황색 번호(①②…)는 그림 아래 범례 번호와 같습니다. 그림을 누르면 크게 볼 수 있습니다.</div>
<div class="warn"><b>책임 한계</b>포털은 근거 조문 · 시행일만 안내합니다. 관경 · 풍량 · 환기량 등 수치 기준과 판정은 각 계산서의 산출근거표와 법령 · 설계기준 원문으로 확인하십시오.</div>
</section>""")
S_.append(f"""<section class="ch" id="ch1"><h2><span class="n">01</span>한눈에 보기</h2>
<p class="lead">설치 없이 브라우저에서 바로 열리는 단일 페이지(PWA)입니다. 입력값이 없고, 연결과 근거 안내만 합니다.</p>
<h3 id="s1-1">1-1. 화면 구성</h3>
{F('s01_overview', '첫 화면')}
{K(T([
 ['머리', '근거 조문 대조일 · 기계설비 기술기준 고시 번호, 포털 이름, 설명'],
 ['요약 5칸', f'계산서 {len(TOOLS)}종(위생 3 · 공조 3 · 열원 2) · KDS 31 · 고시 · PWA · A4'],
 ['탭 막대', '전체 · 위생·배수 · 공조·환기 · 열원·반송 / 근거 법령·기준 / 사용자 매뉴얼'],
 ['계산서 카드', '카드를 누르면 계산서, 「사용자 매뉴얼」을 누르면 그 계산서의 매뉴얼(새 창)'],
 ['근거 법령 · 설계기준', '법령 · 고시 · KDS · 참고 기준 5행 — 현행 번호 · 시행일 · 관련 조문 · 적용 도구'],
], ['영역', '내용']))}
<h3 id="s1-2">1-2. 연결 계산서 8종</h3>
{BR(K(T(tool_rows, ['분류', '번호', '계산서', '버전', '근거 기준', '매뉴얼'])))}
</section>""")
S_.append(f"""<section class="ch" id="ch2"><h2><span class="n">02</span>1분 따라하기</h2>
<p class="lead">예: 다중이용시설의 기계환기 풍량과 덕트 규격을 정하는 현장 — 포털에서 계산서를 찾아 들어가고 근거를 확인하는 순서입니다.</p>
<ol class="steps">
<li><b class="t">① 포털 열기</b>manminkim-eng.github.io/mech-portal — 휴대전화는 「홈 화면에 추가」로 설치합니다.</li>
<li><b class="t">② 분류</b>「공조·환기」 탭을 누르면 냉온수 배관 · 공조 덕트 · 기계환기설비 카드 3장만 남습니다(<a href="#s3-2">3-2</a>).</li>
<li><b class="t">③ 근거 확인</b>기계환기설비 카드의 칩 「설비규칙 제11조 · 별표 1의6」 「기술기준 별표 3」을 확인합니다(<a href="#s3-5">3-5</a>).</li>
<li><b class="t">④ 매뉴얼</b>카드 아래 「사용자 매뉴얼」 — 그 계산서의 매뉴얼이 새 창으로 열립니다.</li>
<li><b class="t">⑤ 계산서</b>카드를 누르면 계산서로 이동해 환기량을 산정하고, 같은 방법으로 공조 덕트 계산서에서 덕트 규격을 정합니다.</li>
<li><b class="t">⑥ 시행일 확인</b>포털 아래 「근거 법령 · 설계기준」 표에서 현행 고시 번호와 시행일을 확인합니다(<a href="#s3-7">3-7</a>).</li>
</ol>
{F('s09_air_tab', '「공조·환기」 탭')}
</section>""")
S_.append(f"""<section class="ch" id="ch3"><h2><span class="n">03</span>화면별 기능</h2>
<h3 id="s3-1">3-1. 머리</h3>
{F('s02_header', '머리')}
<p>맨 위 표시줄은 근거 조문을 국가법령정보와 대조한 날짜({CHECKED})와 기계설비 기술기준의 현행 고시 번호입니다.</p>
<h3 id="s3-2">3-2. 분류 탭</h3>
{F('s03_tabs', '탭 막대')}
<p>「전체 {len(TOOLS)}」 · 「위생·배수 3」 · 「공조·환기 3」 · 「열원·반송 2」는 누르면 해당 묶음만 보여 줍니다. 「근거 법령·기준」은 아래 근거표로 이동하고, 「사용자 매뉴얼」은 이 문서를 새 창으로 엽니다(온라인 전용).</p>
<h3 id="s3-3">3-3. 계산서 카드</h3>
{F('s07_card', '계산서 카드 구성')}
<p>카드 위 번호 「M · 20」은 홈페이지 도구 허브의 공종 표기(M)와 개발 폴더 번호(20)입니다. 버전은 계산서의 현재 판이고, 칩은 그 계산서가 산출근거로 인용하는 법령 · 설계기준입니다.</p>
<h3 id="s3-4">3-4. 위생·배수</h3>
{F('s04_plumb', '위생·배수 카드 3장')}
<h3 id="s3-5">3-5. 공조·환기</h3>
{F('s05_air', '공조·환기 카드 3장')}
<h3 id="s3-6">3-6. 열원·반송</h3>
{F('s06_heat', '열원·반송 카드 2장')}
<h3 id="s3-7">3-7. 근거 법령 · 설계기준</h3>
{F('s08_law', '근거 법령 · 설계기준 표')}
<p>표 아래 안내문은 포털의 원칙(근거 · 시행일만 안내, 수치 기준은 계산서)과 고시 번호의 의미(<a href="#s4-2">4-2</a>)를 적은 것입니다. KDS 원문과 개정 이력은 국가건설기준센터에서 확인합니다.</p>
<h3 id="s3-8">3-8. 휴대전화 화면</h3>
<div class="tri"><div>{fig('s10_mobile_top', '첫 화면', narrow=True)}</div><div>{fig('s11_mobile_card', '카드', narrow=True)}</div><div>{fig('s12_mobile_law', '근거표', narrow=True)}</div></div>
<p>좁은 화면에서는 카드가 한 줄씩 쌓이고, 근거표는 좌우로 밀어서 봅니다.</p>
</section>""")
S_.append(f"""<section class="ch" id="ch4"><h2><span class="n">04</span>근거 해설</h2>
<h3 id="s4-1">4-1. 근거 체계</h3>
{BR(K(T(law_rows, ['법령 · 기준', '구분', '현행', '관련 조문 · 코드', '적용 도구'])))}
<h3 id="s4-2">4-2. 고시 번호 읽는 법</h3>
<p>기계설비 기술기준과 건축물의 에너지절약설계기준의 현행 번호 <b>국토교통부고시 제2026-360호(2026-07-08 시행)</b>는 정부조직 개편 사항을 반영한 57개 고시 일괄 개정(타법개정)입니다. 기계설비 기술기준의 원 고시는 제2021-851호(2021-06-07 발령)이며, 계산서에 이 번호로 적힌 근거는 같은 고시를 가리킵니다.</p>
<h3 id="s4-3">4-3. 포털과 계산서의 역할</h3>
{K(T([
 ['포털', '계산서 진입 · 분류 · 근거 법령과 시행일 · 고시 번호 안내 — 수치 기준을 싣지 않습니다'],
 ['계산서', '입력 · 계산 · 판정 · 산출근거표 · A4 계산서 — 수치 기준과 조항은 계산서가 정본입니다'],
 ['갱신', '법령이 바뀌면 계산서를 먼저 고치고, 포털 근거표는 번호 · 시행일만 고칩니다(데이터 단일 원천 _tools/build_portal.py)'],
], ['구분', '역할']))}
</section>""")
S_.append(f"""<section class="ch" id="ch5"><h2><span class="n">05</span>문제 해결·FAQ</h2>
{K(T([
 ['포털에서 계산이 되나요', '아닙니다 — 카드를 눌러 각 계산서에서 계산합니다'],
 ['「사용자 매뉴얼」이 안 열려요', '매뉴얼은 온라인 전용입니다(오프라인 캐시에서 제외)'],
 ['수치 기준은 어디 있나요', '각 계산서의 산출근거표와 A4 계산서에 있습니다'],
 ['계산서마다 디자인이 달라요', '계산서는 각각 별도 저장소의 도구라 헤드 색과 판이 다를 수 있습니다'],
 ['화면이 예전 판이에요', '새로 고침(Ctrl+F5) 또는 앱을 닫았다 다시 여십시오 — 판이 바뀌면 캐시 이름이 바뀝니다'],
], ['증상', '해결']))}
</section>""")
S_.append(f"""<section class="ch" id="ch6"><h2><span class="n">부록</span></h2>
<h3 id="a1">A1. 버전 변경 내역</h3>
{K(T([
 [f'Ver 1.0.1 · 매뉴얼 {VER} ({DATE})', '사용자 매뉴얼 신설 · 탭 막대 「사용자 매뉴얼」 연결 · sw v1.0.1'],
 ['Ver 1.0.0 (2026-10-29)', '신설 — 계산서 8종 · 분류 3 · 근거 법령 · 설계기준표'],
], ['버전', '내용']))}
<h3 id="a2">A2. 용어</h3>
{BR(K(T([
 ['기계설비 기술기준', '「기계설비법」 제14조에 따른 국토교통부 고시 — 설계 · 시공 기준(별표 1~15)'],
 ['KDS 31', '국가건설기준 설비 설계기준(KDS 31 25 · 31 30 등)'],
 ['타법개정', '다른 법령 · 고시의 개정에 따라 함께 고쳐진 개정 — 내용 개정과 구분'],
 ['PWA', '홈 화면에 설치해 오프라인에서도 여는 웹앱'],
], ['용어', '뜻'])))}
</section>""")
html = render(title=f'{APP} 사용자 매뉴얼 {VER} · MANMIN',
              desc=f'{APP} 사용자 매뉴얼 — 연결 계산서 8종, 근거 법령 · 설계기준 안내',
              eyebrow='MANMIN ENGINEERING · USER MANUAL', h1=f'{APP} 사용자 매뉴얼',
              sub='카드 → 계산서 · 매뉴얼 → 분류 → 근거 법령 · 시행일', ver=VER, date=DATE, app_name='통합 포털',
              pdf=PDF, toc=TOC, sections=S_, foot_note='설비규칙(2026-08-24) · 기계설비 기술기준 · 에너지절약설계기준 제2026-360호(2026-07-08)')
html = html.replace('화면 대응 개정 2026-10-12', '화면 대응 개정 ' + DATE)
open(os.path.join(B, 'index.html'), 'w', encoding='utf-8').write(html)
print('manual ok', len(html))
