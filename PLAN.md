# APD1 1차 진로상담 사이트 — 작업 진행상황

> QA5 `QA_resume_confirm_event`(QA 커리어 나침반)를 참조해 AI 프로덕트 개발 트랙 1기(APD1)용으로 재작성.
> QA 원본 폴더는 수정하지 않음. 작업 시작: 2026-09-14

## 배경 데이터 (확정)
- 레이서 11명: `OneDrive - 엘리스\...KDT_공유폴더\02. KDT 운영\12. APD 트랙\APD 1기\[APD1]레이서_정보.xlsx`
- 커리큘럼·일정: `...\05. KDT 사업개발\05. AI 캠퍼스\02. 커리큘럼\AI캠퍼스_프로덕트개발_강사공유용.xlsx`
- **1차 프로젝트: 2026-09-30(수) 시작 ~ 10-20(화) 발표회** → 상담은 프로젝트 직전 진행
- 상담 방식: 1인당 30분, 1:1
- 희망 진로 3분류: **개발자 / PM / 창업** (+미확정·복수: 김가을, 홍태휘, 황지혜)
- APD1 트랙 로고 컬러: 시안/틸(#10b0f0~#60e0e0 계열) → 사이트 테마도 시안 계열

## 체크리스트

- [x] 요구사항 확정 (진로 3분류, Cal.com 유지, start_guide→상담 준비 가이드, 폴더 위치, 상담기록 신규 양식)
- [x] 소스 데이터 조사 (레이서 정보, 커리큘럼 일정, QA 사이트 구조, APD 로고 색)
- [x] 폴더 생성 (`C:\KDT AX\APD1_OneOnOne`)
- [x] PLAN.md 작성 (이 파일)
- [x] assets 이식 — styles.css(시안 테마 + 3카드 grid + overflow-wrap), script.js, favicon 리컬러(보라→시안)
- [x] index.html (진입: 희망 진로 3카드 + "아직 모르겠어요")
- [x] overview.html (3 페르소나 요약 카드)
- [x] type01.html (개발자 지향)
- [x] type02.html (PM·기획 지향)
- [x] type03.html (창업 지향)
- [x] prep_guide.html (start_guide 대체: 상담 전 준비 가이드)
- [x] booking.html (30분 단일 상담 + Cal.com 임베드 placeholder)
- [x] tools/make_상담기록.py — 통합 1파일 2시트 (상담 로그 + 레이서 프로필)
- [x] [APD1] 1on1 상담 기록.xlsx 생성·검증 (※ 파일명에 `:` 불가 — Windows ADS 함정. `1on1`로 결정)
- [x] README.md (APD1 배포/수정 가이드)
- [x] CLAUDE.md (작업 컨텍스트: 데이터 출처·레이서-진로 매핑·링크 교체 지점)
- [x] 검증: 페이지 링크 흐름 / QA 잔존 텍스트 / CSS 규칙(keep-all+overflow-wrap) / xlsx 구조

## 미해결 (외부 의존)

- [x] **Cal.com 예약 링크 적용 완료 (2026-09-14)** — `cysong/apd1-one-on-one-01`
  - booking.html 2곳: fallback `<a href>` + 임베드 `calLink` 모두 적용됨
  - 추후 이벤트 변경 시 `cysong/apd1-one-on-one-01` 검색 → 2곳 교체
- [ ] 상담 주간 확정 시 booking.html 문구에 기간 반영 (현재: "1차 프로젝트 시작(9/30) 전" 표현)
- [ ] 운영매니저 GitHub/Vercel 배포 (QA와 동일 절차 — README.md 참조)

## 수정 이력

- **2026-09-14 7차 (원격 저장소 변경)**
  - 배포 원격을 `c0song/apd1-1on1-session` → `chanyoung0809/apd-career-compass`로 변경 (QA 원본과 동일 계정 체계)
  - 기존 c0song 저장소는 운영 기록으로 남김 (삭제는 운영매니저 판단)
- **2026-09-14 6차 (GitHub push)**
  - 저장소: https://github.com/c0song/apd1-1on1-session (main, 초기 push)
  - `[APD1] 1on1 상담 기록.xlsx`는 레이서 개인정보(지원동기·수료후목표 원문) 포함 → .gitignore로 저장소 제외, 운영 PC 로컬 전용
  - tools/make_상담기록.py: 개인 OneDrive 폴더명 하드코딩 제거, 공유폴더 자동 탐색(`*KDT_공유폴더*` glob)으로 리팩터. 실행 재검증 완료
- **2026-09-14 5차 ("팀" 표기 제거)**
  - 1차 프로젝트의 개인/팀 진행 방식이 미확정이라, 공개 페이지의 "팀 과제·팀 웹앱·팀 회의" 등 표기 12곳을 중립적 "프로젝트" 표현으로 교체 (type01/02/03, overview, prep_guide)
  - 협업·역할 같은 일반 단어는 유지. 방식 확정 시 다시 구체화 가능
- **2026-09-14 4차 (커리큘럼 순서 정정)**
  - AI API·LLM 연동: "1차 프로젝트 이후" → "**1차 프로젝트 직전 과정**"으로 정정 (type01/02/03 학습 현황)
  - 상담 주간 = 프론트엔드~백엔드 학습 구간임을 type02에 명시
  - 서비스 기획·요구사항 정의(PRD)·AI 기능 설계 등 기획 과목은 1차 프로젝트 이후 (기존 표기 유지)
- **2026-09-14 3차 (상담 시간 옵션·학습 범위)**
  - 상담 시간: 30분(기본 권장) + 60분(할 말이 많을 때 선택) 2카드 안내로 변경. 예약은 단일 Cal.com 이벤트(`cysong/apd1-one-on-one-01`)에서 레이서가 길이를 선택하는 구조
  - 학습 범위 표기 보정: 현재 완료·근시일 범위는 프론트엔드~백엔드(HTML/CSS·React, FastAPI·DB)까지. AI API·LLM 연동·AI 기능 설계·서비스 기획(PRD) 과목은 1차 프로젝트 이후 과정임을 type01/02/03 spec과 type02 액션플랜에 반영
  - CSS: 시간 카드 grid 2열 전환(--single 블록 제거), 60분 카드 mint 구분색
- **2026-09-14 2차 (개인정보·윤문·링크)**
  - 공개 페이지에서 개인 식별 가능한 발췌 제거: 구체 아이템명('가치잇다'·ERP 등), 개인 경력 상세(북클럽 3년·창업학회 앱·항공 서비스 등), 전공 목록 → "비전공자인 경우가 많아요" 식 뭉뚱그린 표현으로 교체. 구체 데이터는 상담 기록 xlsx(운영 내부용)에만 유지
  - 긴 작대기(—) 전부 제거 (HTML 4개 파일 11곳)
  - Cal.com 실제 링크 `cysong/apd1-one-on-one-01` 2곳 적용, 미설정 경고 주석 제거

## 설계 결정 기록

| 항목 | 결정 | 이유 |
|---|---|---|
| 진로 페이지 | type01(개발자)/type02(PM)/type03(창업) | QA의 type01~04 패턴 유지, 3개로 축소 |
| start_guide.html | prep_guide.html로 교체 | 1차 프로젝트 전 상담이라 이력서 가이드 부적합 |
| 예약 임베드 | Cal.com `cysong/apd1-one-on-one-01` 확정 적용 | 사용자 제공 링크 2곳(fallback+calLink)에 반영 완료 |
| 테마 색 | QA 핑크→APD 시안 | APD1 트랙 로고 dominant 색 반영 |
| 개인정보 | 공개 페이지는 뭉뚱그린 표현만 | 구체 아이템명·경력은 상담 기록 xlsx(내부용)에만 |
| 상담 기록 | 통합 1파일(로그+프로필 2시트) | 구버전 개인별 11파일 방식은 "구려서 미사용" 이력 → 관리 편한 통합형으로 신규 설계 |
| favicon | reserv_favicon.png alpha 보존 리컬러 | QA CLAUDE.md의 recolor 패턴 적용 |
