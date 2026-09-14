# APD 커리어 나침반 — 작업 컨텍스트

APD1(AI 프로덕트 개발 트랙 1기) 레이서 대상 1차 진로상담 정적 사이트. 운영매니저(KDT)가 직접 운영/수정.
QA5 `QA_resume_confirm_event`(QA 커리어 나침반)를 참조해 2026-09-14에 재작성함.

## 배경

- 목적: 1차 프로젝트(2026-09-30 시작 ~ 10-20 발표회)를 앞두고, 레이서 11명의 **희망 진로와 프로젝트 고민**을 파악하기 위한 1:1 상담(1인당 30분) 안내.
- 희망 진로 3분류: **개발자 / PM / 창업** (+ 미확정·복수).
- 예약: Cal.com 임베드(30분 단일) — `cysong/apd1-one-on-one-01` 확정 적용됨 (2026-09-14).

## 데이터 출처 (읽기 전용 원본)

- 레이서 정보: `OneDrive - 엘리스\...\02. KDT 운영\12. APD 트랙\APD 1기\[APD1]레이서_정보.xlsx` (11명, 지원동기·수료후목표·희망직무 포함)
- 커리큘럼·일정: `OneDrive - 엘리스\...\05. KDT 사업개발\05. AI 캠퍼스\02. 커리큘럼\AI캠퍼스_프로덕트개발_강사공유용.xlsx`
  - 1차 프로젝트: Week 5 (09/30) 시작, Week 7 (10/20) 발표회 — `_(개강연기)과정3_시간표` 시트 기준
  - 과정3 기술 스택: HTML/CSS, React/Vue, FastAPI(백엔드), DB·ORM, AI API·LLM 연동, AI 기능 설계, 배포·운영
- 참조 원본 사이트: `C:\KDT AX\QA5_team_project_01\1차 진로상담 시트\QA_resume_confirm_event` (수정 금지, 참조 전용)

## 페이지 구조

루트의 7개 HTML이 운영 페이지:

- `index.html` — 진입. "나의 희망 진로는?" 3카드 + "아직 모르겠어요" → prep_guide
- `type01.html` — 개발자 지향 (💻, data-type="01")
- `type02.html` — PM·기획 지향 (🧩, data-type="02")
- `type03.html` — 창업 지향 (🚀, data-type="03")
- `overview.html` — 3 유형 요약 카드
- `prep_guide.html` — 상담 전 준비 가이드 (QA의 start_guide.html 대체)
- `booking.html` — 30분 단일 상담 예약, Cal.com 임베드

공용 자산: `assets/css/styles.css`, `assets/js/script.js`, `assets/images/`.
`tools/make_상담기록.py` → `[APD1] 1on1 상담 기록.xlsx` (통합 2시트: 상담 로그 + 레이서 프로필).

## 레이서-진로 사전 매핑 (상담 기록 '사전 추정' 칸과 동일)

| 진로 | 레이서 |
|---|---|
| 개발자 | 김호림, 이현진(창업 병행), 전세황, 정우현 |
| PM | 김서연 |
| 창업 | 박서현(가치잇다), 서지훈(ERP→AI), 최은비(1인 MVP) |
| 미확정·복수 | 김가을, 홍태휘, 황지혜 |

## Cal.com 링크 (설정 완료)

`booking.html`에 `cysong/apd1-one-on-one-01` 링크가 **2곳**에 설정됨 (fallback `<a href>` + 임베드 `calLink`).
이벤트 변경 시: `cysong/apd1-one-on-one-01` 검색 → 2곳 교체. 임베드 `calLink`에는 `아이디/이벤트이름` 형식만 (https://cal.com/ 포함 금지).

## 개인정보 원칙 (헷갈리기 쉬운 부분)

공개 사이트(HTML)에는 레이서 개인의 구체 아이템명·경력·전공을 쓰지 않는다 — "비전공자인 경우가 많아요"처럼 뭉뚱그린 표현만.
구체 데이터(아이템명, 경력 상세, 지원동기·수료후목표 원문)는 `[APD1] 1on1 상담 기록.xlsx`(운매니저 내부용)에만 둔다.

## Favicon

`assets/images/reserv_favicon.png` — 예약 체크 아이콘을 QA 보라(#6700e6)에서 **APD 시안(#10b0f0)으로 재색칠**한 것.
HTML 7개의 `<head>`에 동일하게 참조됨:

```html
<link rel="icon" type="image/png" href="assets/images/reserv_favicon.png">
<link rel="apple-touch-icon" href="assets/images/reserv_favicon.png">
```

### PNG recolor 패턴 (alpha 보존)

단색 아이콘 PNG의 색만 바꿔야 할 때 — alpha 채널은 유지하고 RGB만 통일:

```bash
python -c "from PIL import Image; im = Image.open('FILE.png').convert('RGBA'); px = im.load(); w,h = im.size; r,g,b = 0x10,0xb0,0xf0; [px.__setitem__((x,y), (r,g,b,px[x,y][3])) for x in range(w) for y in range(h) if px[x,y][3] > 0]; im.save('FILE.png')"
```

## 테마 색 (QA 핑크 → APD 시안)

- primary `#2bb8ea` / secondary `#6fd4f2` / 배경 `#f4fbff` — APD1 트랙 로고 dominant 색(#10b0f0~#60e0e0) 반영
- type별 accent: 01 개발자 sky `#a8e6f7` / 02 PM periwinkle `#c9c8f7` / 03 창업 mint `#a8e6cf`
- 다크모드 대응 규칙 포함(prefers-color-scheme: dark). QA 원본과 구조 동일, 색만 치환.

## 배포

- 미배포 상태. QA처럼 **GitHub 신규 repo + Vercel** 절차 권장 — `README.md` 3-1/6장 참조 (fork 불필요, 이 폴더를 새 repo로 업로드).
- 배포 시 Vercel Framework Preset은 `Other`, Root Directory 변경 없음.
