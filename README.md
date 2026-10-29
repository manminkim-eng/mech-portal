# 기계설비 계산서 통합 포털 (mech-portal) — Ver 1.0.0

- 신설: 2026-10-29 · Engineer KIM MANMIN · ㈜대성건축사사무소
- 성격: 소방 통합 포털(portal v5.2.0)과 같은 형식의 공종 통합 포털 — 기계설비 계산서 8종(20~27) 바로가기 + 근거 법령·설계기준 안내
- 원칙: 포털에는 근거 조문·시행일만 싣고 수치 기준은 각 계산서에 둔다(2026-10-29 MIN 승인).
- 데이터 단일 원천: `_tools/build_portal.py` 의 TOOLS · LAWS → `python _tools/build_portal.py` 로 index.html 재생성
- 근거 대조(2026-10-29, LawMCP): 건축물의 설비기준 등에 관한 규칙(2026-08-24 시행) · 기계설비 기술기준(국토교통부고시 제2026-360호, 2026-07-08 시행, 타법개정) · 건축물의 에너지절약설계기준(제2026-360호, 2026-07-08 시행). KDS 명칭은 기계설비 기술기준 별표 각 1.3 표기.
- 배포 경로(예정): https://manminkim-eng.github.io/mech-portal/  (저장소 `manminkim-eng/mech-portal` 신규 생성 필요)
- 구성: index.html · manifest.json · sw.js(캐시 접두어 manmin-mech-portal-) · icons/ · assets/fonts/(로컬 폴백) · _tools/
