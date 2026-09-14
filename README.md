# APD 커리어 나침반 — APD1 운영매니저용 제작/배포 가이드

이 문서는 **개발이나 영어가 익숙하지 않은 운영매니저**도 동일한 형식의 진로상담 안내 페이지를
만들고, 무료로 인터넷에 공개할 수 있도록 단계별로 안내합니다.

참조 원본: QA5 트랙의 `QA_resume_confirm_event` (QA 커리어 나침반, https://github.com/chanyoung0809/qa-career-compass)

---

## 1. 이 사이트가 무엇을 하는 페이지인가요

AI 프로덕트 개발 트랙 1기(APD1) 레이서의 **희망 진로(개발자 / PM / 창업)**에 따라
맞춤 안내와 운영매니저 1:1 상담(30분) 예약으로 연결해 주는 **정적 HTML 사이트**입니다.

1차 프로젝트(2026-09-30 시작 ~ 10-20 발표회)를 앞두고 진행하는 상담용입니다.

페이지 흐름은 아래와 같습니다.

```
index.html (메인 진입: "나의 희망 진로는?")
  ├─ 💻 개발자        → type01.html
  ├─ 🧩 PM·기획       → type02.html
  ├─ 🚀 창업          → type03.html
  │       └─ 각 유형 페이지 하단에서 booking.html 로
  │
  └─ 🤔 "아직 모르겠어요" → prep_guide.html (상담 전 준비 가이드)
                               └─ booking.html 로 연결

booking.html  ← Cal.com 1:1 예약 캘린더(30분)가 임베드되어 있음
```

서버나 데이터베이스 없이 **HTML 파일만으로 동작**하기 때문에,
무료로 빠르게 배포할 수 있습니다.

---

## 2. 폴더 구조 — 어떤 파일을 만지면 어디가 바뀌나요

```
APD1_OneOnOne/
├── index.html          ← 첫 화면. 희망 진로 3개 카드 + "아직 모르겠어요"
├── overview.html       ← 3가지 진로 유형 카드 모음
├── type01.html         ← 개발자 지향 상세
├── type02.html         ← PM·기획 지향 상세
├── type03.html         ← 창업 지향 상세
├── prep_guide.html     ← 상담 전 준비 가이드 (고민 3줄 메모법)
├── booking.html        ← Cal.com 1:1 상담 예약 (★ Cal.com 연결 부분)
├── PLAN.md             ← 작업 진행상황 기록
├── [APD1] 1on1 상담 기록.xlsx  ← 상담용 기록 양식 (생성물, 로컬 전용: 저장소 제외)
├── tools/
│   └── make_상담기록.py  ← 상담 기록 양식 재생성 스크립트
└── assets/
    ├── css/styles.css  ← 색상, 폰트, 카드 디자인 등 전체 디자인
    ├── js/script.js    ← 카드 클릭 같은 사소한 동작
    └── images/reserv_favicon.png  ← favicon (APD 시안색으로 재색칠됨)
```

**문구만 바꾸고 싶다면** 각 `.html` 파일을 열어 따옴표 또는 태그 사이의
한국어 텍스트만 수정하면 됩니다. CSS는 건드리지 않아도 디자인이 그대로 적용됩니다.

> 메모장보다는 [VS Code](https://code.visualstudio.com/) (무료) 사용을 권장합니다.
> 한국어가 깨지지 않고 색깔로 코드가 구분되어 훨씬 편합니다.

---

## 3. 본인 버전 만들기 — 단계별 가이드

### 사전 준비물 (모두 무료)

| 항목 | 용도 | 가입 링크 |
| --- | --- | --- |
| GitHub 계정 | 코드 저장소 | https://github.com/signup |
| GitHub Desktop | GitHub를 클릭만으로 다루기 | https://desktop.github.com/ |
| Cal.com 계정 | 1:1 예약 캘린더 | https://cal.com/signup |
| Vercel 계정 | 무료 배포 (GitHub 계정으로 로그인 가능) | https://vercel.com/signup |
| VS Code | 텍스트 수정용 에디터 | https://code.visualstudio.com/ |

### 3-1. GitHub에 새 저장소 만들고 폴더 올리기

QA 버전과 달리 원본 repo를 fork할 필요가 없습니다. 이 폴더 전체를 새 repo로 올리면 됩니다.

1. https://github.com/new 접속 → 저장소 이름 입력 (예: `apd-career-compass`) → **Create repository**
2. GitHub Desktop 실행 → **File → Add local repository** → 이 폴더(`APD1_OneOnOne`) 선택
   - "not a git repository" 안내가 뜨면 **Create a Repository** 클릭 후 추가
3. 좌측 하단 Summary에 `최초 업로드` 작성 → **Commit to main** → 상단 **Publish repository** 클릭

### 3-2. 내용 수정하기

VS Code로 폴더를 열고, 각 HTML 파일에서 다음과 같은 부분만 수정합니다.

- **사이트 제목**: `<title>` 태그와 `<h1>` 태그 안의 문장
- **진로 유형 설명**: type01~03.html 안의 본문 문구
- **상담 안내 문구**: booking.html 안의 안내 단락
- **이미지/이모지**: 그대로 두거나 원하는 이모지로 교체

> 처음에는 텍스트만 바꿔 보세요. 구조나 태그(`<div>`, `<span>` 등)는
> 건드리지 않는 것이 안전합니다.

---

## 4. Cal.com 1:1 예약 캘린더 연결하기 (가장 중요)

`booking.html` 페이지의 캘린더는 Cal.com의 **임베드 기능**으로 표시됩니다.

### 4-1. Cal.com 이벤트 만들기

1. https://cal.com 가입 후 로그인
2. 좌측 메뉴 **Event Types** → 우측 상단 **+ New** 클릭
3. **30분 상담** 이벤트 1개를 만듭니다 (APD1은 1인당 30분 단일 운영).
   - 예: 제목 "APD1 1차 진로상담 (30분)", 길이 30분
4. 이벤트의 **Event Link**(URL의 마지막 부분)를 메모해 둡니다.
   예: `https://cal.com/내아이디/apd1-one-on-one` → 식별자는 `내아이디/apd1-one-on-one`

### 4-2. booking.html의 Cal.com 링크 (설정 완료)

현재 `booking.html`에는 **`cysong/apd1-one-on-one-01`** 링크가 설정돼 있습니다.
다른 이벤트로 바꾸려면 `booking.html`을 열어 `cysong/apd1-one-on-one-01`을 검색하세요. **딱 2곳**이 나옵니다:

```html
<!-- (1) 새 창으로 여는 fallback 링크 -->
<a href="https://cal.com/cysong/apd1-one-on-one-01" ...>새 창에서 예약 페이지 열기</a>

<!-- (2) 인라인 임베드 -->
calLink: "cysong/apd1-one-on-one-01"   // ← 이 부분
```

바꾸는 방법:
- (1)은 `https://cal.com/`를 포함한 전체 주소를, (2)에는 `아이디/이벤트이름` 형식만 넣습니다.
- Cal.com에서 30분 상담 이벤트를 만들고, 그 이벤트의 식별자로 바꾸면 됩니다.

### 4-3. 상담 안내 문구 수정 (선택)

`booking.html`의 "1차 진로 상담주간 안내" 단락에는 상담 기간·준비물·진행 방식이 적혀 있습니다.
운영 일정에 맞춰 자유롭게 수정하세요.

---

## 5. GitHub에 변경사항 올리기

1. GitHub Desktop으로 돌아가면 좌측에 수정된 파일 목록이 보입니다.
2. 좌측 하단 **Summary** 칸에 변경 내용을 한 줄로 적습니다.
   예: `Cal 링크 교체`
3. **Commit to main** 버튼 클릭
4. 상단 **Push origin** 버튼 클릭 → GitHub에 업로드 완료

---

## 6. Vercel로 배포하기 (무료 도메인)

### 6-1. Vercel에 GitHub 계정으로 로그인

1. https://vercel.com/login → **Continue with GitHub** 클릭
2. GitHub 권한 승인

### 6-2. 프로젝트 Import

1. https://vercel.com/new 접속
2. **Import Git Repository** 목록에서 새로 만든 repo(예: `apd-career-compass`) 옆 **Import** 클릭
3. Configure Project 화면 설정:
   - **Project Name**: 원하는 이름 (이게 곧 `{이름}.vercel.app` 주소가 됩니다)
   - **Framework Preset**: `Other`
   - **Root Directory**: 변경하지 않음
   - **Build & Output Settings**: 그대로 두기 (정적 사이트라서 빌드 불필요)
4. **Deploy** 클릭 → 1~2분 후 배포 완료

### 6-3. 도메인 확인 및 변경

- 기본 도메인: `프로젝트명.vercel.app`
- 더 짧게 바꾸고 싶다면 Vercel 프로젝트 화면 **Settings → Domains** 에서 변경

### 6-4. 이후 업데이트는 자동

GitHub Desktop으로 변경사항을 **Push origin** 하면, Vercel이 자동으로 감지해
1~2분 안에 다시 배포합니다. 별도 작업 불필요.

---

## 7. 상담 기록 양식 관리 (tools/)

- `[APD1] 1on1 상담 기록.xlsx` — 11명 통합 양식 (**⚠️ 레이서 개인정보가 들어 있어 GitHub 저장소에는 제외** — `.gitignore` 참조. 운영 PC에만 두세요)
  - **상담 로그** 시트: 레이서별 사전 추정 진로·핵심 목표가 자동 채워져 있고, 상담 일시/내용/고민 키워드/액션 아이템/후속 조치 칸은 상담 중 직접 작성
  - **레이서 프로필** 시트: 지원동기·수료후목표 원문 (상담 직전 읽기용)
- 양식을 다시 뽑고 싶으면: `python tools/make_상담기록.py`
  ⚠️ 상담 메모 입력 후 재실행하면 메모가 사라집니다. 반드시 백업 후 실행.

---

## 8. 자주 묻는 질문

**Q. 코드를 만지는 게 무서워요. 망가지면 어떡하죠?**

GitHub Desktop의 좌측 상단 **History** 탭에서 언제든 이전 시점으로 돌아갈 수 있어요.

**Q. 캘린더가 안 떠요.**

`booking.html` 안의 `calLink` 부분이 본인 Cal.com 링크 식별자와 정확히 일치하는지 확인하세요.
앞에 `https://cal.com/` 같은 주소까지 적으면 동작하지 않습니다. **아이디/이벤트이름** 형식만 남겨야 합니다.
`calLink` 앞에 `https://cal.com/`까지 적으면 캘린더가 뜨지 않습니다. **아이디/이벤트이름** 형식만 남겨야 합니다.

**Q. 한글이 깨져요.**

파일을 저장할 때 인코딩이 **UTF-8** 이어야 합니다. VS Code는 기본값이 UTF-8이므로 안전합니다.

**Q. Vercel 무료 플랜으로 충분한가요?**

운영 안내 페이지 수준의 트래픽이라면 충분합니다.
월 100GB 대역폭, 무제한 배포가 무료 제공됩니다.

**Q. Cal.com 무료 플랜으로 충분한가요?**

1:1 예약은 무료 플랜으로 무제한 사용 가능합니다.

---

## 9. 도움이 필요할 때

- 이 페이지를 만든 사람에게 직접 문의 (slack/메일)
- GitHub 사용법: https://docs.github.com/ko (한국어 공식 문서)
- Cal.com 사용법: https://cal.com/help
- Vercel 사용법: https://vercel.com/docs (한국어 일부 제공)

---

## 라이선스 / 사용 안내

본 페이지의 문구와 디자인은 엘리스 AI 프로덕트 개발 트랙 운영팀 내부 사용을 위해 제작되었습니다.
QA5 트랙의 `QA_resume_confirm_event`(QA 커리어 나침반)를 참조해 재작성되었습니다.
구조와 코드를 참고하여 본인 운영용 페이지로 자유롭게 변경해 사용하세요.
