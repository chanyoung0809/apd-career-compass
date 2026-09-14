# -*- coding: utf-8 -*-
"""APD1 1:1 진로상담 기록 양식 자동 생성

용도
- APD1(AI 프로덕트 개발 트랙 1기) 1차 진로상담(1인당 30분)을 위해 통합 1파일 양식을 생성합니다.
  - 시트 '상담 로그'      : 활동 레이서 한 줄씩. 사전 추정 진로·핵심 목표는 자동 채움, 상담 기록 칸은 빈칸.
  - 시트 '레이서 프로필'  : 지원동기·수료후목표 원문. 상담 직전 읽기용.
  - 시트 'NN_이름' (개인별): 1인당 1시트. 표지·프로젝트 일정·배경 데이터·원문·진로별 질문 가이드
                            + 상담 중 기록 칸. 상담 중 이 시트를 열어 씁니다.
- 데이터 출처: [APD1]레이서_정보.xlsx (OneDrive KDT_공유폴더 12. APD 트랙\\APD 1기)
- 제외 대상: [APD1] 출석부.xlsx의 '중도탈락'·'수강철회' 시트에 있는 레이서.
  출석부를 못 읽으면(파일 잠김 등) 하단 EXCLUDE_FALLBACK 명단으로 대체합니다.

주의
- 이 스크립트를 다시 실행하면 출력 파일이 덮어쓰기됩니다.
- 상담 메모(상담 로그·개인별 시트)가 입력된 후에는 재실행을 피하세요. 필요 시 백업 후 실행.
"""
import glob
import os
import sys
import io

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# KDT 공유폴더(OneDrive) 안에서 레이서 정보 파일을 자동 탐색
_SHARE = glob.glob(os.path.join(os.path.expanduser("~"), "OneDrive - 엘리스", "*KDT_공유폴더*"))
if not _SHARE:
    raise SystemExit("OneDrive KDT_공유폴더를 찾지 못했습니다. 폴더명을 확인하세요.")
RACER_XLSX = os.path.join(
    _SHARE[0], "02. KDT 운영", "12. APD 트랙", "APD 1기", "[APD1]레이서_정보.xlsx"
)
OUT_XLSX = r"C:\KDT AX\APD1_OneOnOne\[APD1] 1on1 상담 기록.xlsx"

# 상담 사이트 저장소 (Vercel 배포 완료 후 "https://<프로젝트>.vercel.app"로 교체)
SITE_REPO_URL = "https://github.com/chanyoung0809/apd-career-compass/blob/main"

# 출석부.xlsx를 읽지 못했을 때 사용하는 백업 명단 (2026-09-14 출석부 기준)
EXCLUDE_FALLBACK = {"박서현", "김서연", "서지훈", "최은비"}


def load_excluded():
    """출석부.xlsx의 중도탈락·수강철회 시트에서 제외 명단을 읽습니다."""
    import shutil
    import tempfile

    import pandas as pd

    try:
        src = os.path.join(os.path.dirname(RACER_XLSX), "[APD1] 출석부.xlsx")
        tmp = os.path.join(tempfile.gettempdir(), "apd1_attendance_copy.xlsx")
        shutil.copy2(src, tmp)  # 운영 중 파일 잠김 방지: 임시 복사본으로 읽기
        names = set()
        for sheet in ("중도탈락", "수강철회"):
            df = pd.read_excel(tmp, sheet_name=sheet, header=4)
            if "이름" in df.columns:
                names |= {str(v).strip() for v in df["이름"].dropna()}
        if names:
            return names, "출석부.xlsx 중도탈락·수강철회 시트"
    except Exception as e:
        print(f"  · 출석부 읽기 실패({type(e).__name__}) → 백업 명단 사용")
    return set(EXCLUDE_FALLBACK), "백업 명단 (EXCLUDE_FALLBACK)"


# 진로 그룹별 상담 체크리스트·질문 가이드 (사이트 type01/02/03·prep_guide 문구 기반)
CAREER_GUIDE = {
    "dev": [
        "1차 프로젝트에서 맡고 싶은 파트 — 프론트(React) / 백엔드(FastAPI·DB) / AI 기능 중 어디?",
        "지금 가장 손에 안 익는 기술은? 9/30 프로젝트 시작 전 보완 방법 정리",
        "\"AI에 의존한 코드 아니에요?\" — AI는 초안, 설계·판단은 본인이라는 1분 답변 연습 여부",
        "채용공고 × 트랙 커리큘럼 매핑표 — 신입 개발자 공고 3개의 요구 스택 확인 여부",
        "포트폴리오 방향 — '돌아가는 결과물 1개' + README·데모·커밋 기록으로 증명",
        "트랙 경험을 이력서에 쓰는 방식 — 어디까지 '실무 경험'으로 쓸 수 있을지",
    ],
    "pm": [
        "개발자와의 대화에서 막히는 지점 — '보기 좋게' 같은 애매 표현을 구체 명세로 바꾸는 연습",
        "1차 프로젝트에서 PRD 한 장 — 요구사항·우선순위·완료 기준을 먼저 써 볼 계획",
        "AI 기능 설계 근거표 — 기능 후보 × 해결 문제 × 꼭 필요한 이유 × 검증 방법",
        "\"기획자가 왜 개발 트랙을 나왔나\" — 1분 스크립트 초안 작성",
        "신입 PM 채용 경로 — 경력 우대 공고 속 첫 발 디딜 경로 (인턴·사이드 프로젝트 등)",
        "기획 과목(PRD·AI 기능 설계)은 1차 프로젝트 이후 — 그때까지 기획 감각 준비 방법",
    ],
    "startup": [
        "아이템 한 문장 정의 — 누가 / 어떤 문제를 / 이 기능으로 / 어떻게 해결하는지 4칸",
        "Must / Nice 기능 분리 — '없으면 서비스가 아닌' 기능 1개 찾기",
        "1차 프로젝트에 녹일 검증 가설 1개 — AI 요약·추천·챗봇 등 주제와의 공통점 찾기",
        "MVP 범위 — '일주일 안에 만들 수 있는 최소 버전'으로 좁히기",
        "AI 신뢰성(환각·오류) 대응 — 사용자가 믿고 쓸 MVP의 조건",
        "수료 후 시간·자금 계획 — MVP 구현·검증까지의 로드맵",
    ],
    "unsure": [
        "3줄 메모 확인 — 끌리는 진로+이유 / 가장 큰 걱정 / 꼭 물어볼 질문 1개",
        "개발자·PM·창업 각각 끌림도(1~5)와 한 줄 이유",
        "지금까지 가장 재밌었던 과목·가장 어려웠던 과목 — 진로 감각의 힌트",
        "1차 프로젝트에서 맡고 싶은 파트 — 직접 해보면서 진로를 좁히는 방법",
        "유형 페이지(type01~03) 읽어 본 뒤 — 공감되는 문구·안 맞는 문구",
        "수료후목표를 본인 말로 한 문장 정리",
    ],
}

# 복수·병행 진로자에게 추가로 넣어주는 보조 항목 (주 진로 가이드 뒤에 붙음)
SECONDARY_GUIDE = {
    "이현진": [
        "[창업 지향 참고] 아이템 한 문장 정의(4칸) + 1차 프로젝트에 검증 가설 1개 녹이기",
    ],
    "황지혜": [
        "[개발 지향 참고] 맡고 싶은 파트(프론트/백엔드) 미리 정해 오기",
        "[PM 지향 이유] '취업한다면 PM쪽 생각하고 있습니당' (Discord 9/2 원문)",
    ],
}

TYPE_PAGE = {
    "dev": ("type01.html — '개발자 지향' 편 (💻)", "type01.html"),
    "pm": ("type02.html — 'PM·기획 지향' 편 (🧩)", "type02.html"),
    "startup": ("type03.html — '창업 지향' 편 (🚀)", "type03.html"),
    "unsure": ("overview.html — 3 유형 요약 → type01~03 전체 (🤔)", "overview.html"),
}

TAB_COLOR = {"dev": "A8E6F7", "pm": "C9C8F7", "startup": "A8E6CF", "unsure": "D9D9D9"}

# 레이서 정보 시트의 수료후목표를 상담용으로 요약한 것 (상담 로그 B영역 자동 채움용)
CORE_GOAL = {
    "김가을": "배운 내용을 프로젝트에 적용, 포트폴리오 완성 후 새 직무로 전환",
    "김서연": "AI 활용 서비스기획·PM으로 커리어 확장 (메디컬 도메인 특화)",
    "김호림": "AI 서비스 개발 관련 직무 취업 (가장 우선적인 목표)",
    "박서현": "지역 상생 플랫폼 '가치잇다'를 MVP로 구현 후 사용자 검증",
    "서지훈": "직접 설계해 온 ERP 시스템을 운영 가능한 AI 서비스로 완성",
    "이현진": "머리 속 아이디어를 직접 실행해 저만의 프로덕트 개발",
    "전세황": "프론트(React/Vue)·백엔드(FastAPI)·DB 실무 역량으로 웹앱 개발 취업",
    "정우현": "AI 서비스 개발 실무 역량·프로젝트 경험을 갖춰 개발 직무 취업",
    "최은비": "AI 개발 기술×비즈니스 설계로 1인 창업 MVP를 직접 개발·검증",
    "홍태휘": "취업 최종합격 (구체 계획 미정 → 상담에서 목표 정리 필요)",
    "황지혜": "기획에서 멈추지 않고 직접 설계·구현해 출시까지 해보는 것",
}

# 지원서·수강목적 기준 사전 추정 진로 (상담에서 확정 칸을 따로 둠)
PRE_ESTIMATE = {
    "김가을": "미확정 (이직 목표, 직무 미정)",
    "김서연": "PM (서비스기획 전환 희망)",
    "김호림": "개발자 (AI 서비스 개발 취업)",
    "박서현": "창업 ('가치잇다' MVP)",
    "서지훈": "창업 (AI 서비스 완성)",
    "이현진": "개발자 (풀스택, 창업 병행)",
    "전세황": "개발자 (웹앱 개발 취업)",
    "정우현": "개발자 (AI 서비스 개발 취업)",
    "최은비": "창업 (1인 MVP, PM 병행)",
    "홍태휘": "미확정 (취업 목표)",
    "황지혜": "미확정·복수 (개발·PM 모두 흥미) — 취업 시 PM 지향 (Discord 9/2)",
}

# 사전 추정 문자열과 달리 질문 가이드를 별도 그룹으로 뽑아줄 레이서 (group_of 최우선 적용)
GROUP_OVERRIDE = {
    "황지혜": "pm",  # 취업 경로가 PM 지향(Discord 9/2)이라 PM 가이드를 주로 사용 + 개발 참고 보조
}

HEAD_FILL = PatternFill("solid", fgColor="2BB8EA")
HEAD_FONT = Font(bold=True, color="FFFFFF", size=11)
THIN = Side(style="thin", color="C9D8E2")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP_TOP = Alignment(vertical="top", wrap_text=True)
WRAP_CENTER = Alignment(vertical="center", horizontal="center", wrap_text=True)


def load_racers():
    import pandas as pd

    df = pd.read_excel(RACER_XLSX, header=1)
    df = df[df["이름"].notna()]
    rows = []
    for _, r in df.iterrows():
        name = str(r["이름"]).strip()
        rows.append({
            "이름": name,
            "전공": fmt(r["학과/전공"]),
            "재직 상태": fmt(r["재직 상태"]),
            "현재 직무": fmt(r["현재 직무"]),
            "희망 직무": fmt(r["희망 직무"]),
            "수강목적": fmt(r["수강목적"]),
            "지원동기": fmt(r["지원동기"]),
            "수료후목표": fmt(r["수료후목표"]),
        })
    return rows


def fmt(v, default="—"):
    s = "" if v is None else str(v).strip()
    if not s or s.lower() == "nan":
        return default
    return s.replace("\r\n", "\n")


def style_sheet(ws, widths, height_first_col=2):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for cell in ws[1]:
        cell.fill = HEAD_FILL
        cell.font = HEAD_FONT
        cell.alignment = WRAP_CENTER
        cell.border = BORDER
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP_TOP
            cell.border = BORDER
    ws.freeze_panes = "C2"
    ws.row_dimensions[1].height = 30


def current_status(r):
    status = r["재직 상태"] if r["재직 상태"] != "—" else "취업 준비생"
    if r["현재 직무"] != "—":
        status += f" · {r['현재 직무']}"
    return status


def group_of(name):
    if name in GROUP_OVERRIDE:
        return GROUP_OVERRIDE[name]
    e = PRE_ESTIMATE.get(name, "")
    if e.startswith("개발자"):
        return "dev"
    if e.startswith("PM"):
        return "pm"
    if e.startswith("창업"):
        return "startup"
    return "unsure"


def build_individual_sheet(wb, r, i):
    name = r["이름"]
    group = group_of(name)
    page_text, page_file = TYPE_PAGE[group]
    ws = wb.create_sheet(f"{i:02d}_{name}")
    ws.sheet_properties.tabColor = TAB_COLOR[group]
    ws.column_dimensions["A"].width = 19
    ws.column_dimensions["B"].width = 95
    ws.freeze_panes = "A2"

    ws.row_dimensions[1].height = 30
    ws.merge_cells("A1:B1")
    title = ws.cell(row=1, column=1, value=f"{i:02d} · {name} — 1:1 진로상담 시트 (30분)")
    title.fill = HEAD_FILL
    title.font = HEAD_FONT
    title.alignment = Alignment(vertical="center")

    row = 3

    def sec(title, note=None):
        nonlocal row
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=2)
        c = ws.cell(row=row, column=1, value=title)
        c.fill = PatternFill("solid", fgColor="D9F0FB")
        c.font = Font(bold=True, color="17607E", size=11)
        c.alignment = Alignment(vertical="center")
        ws.cell(row=row, column=2).border = BORDER
        c.border = BORDER
        row += 1
        if note:
            ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=2)
            n = ws.cell(row=row, column=1, value=note)
            n.font = Font(color="73838E", italic=True, size=9)
            n.alignment = Alignment(vertical="top", wrap_text=True)
            ws.row_dimensions[row].height = 14
            row += 1

    def item(label, value, height=None, link=None):
        nonlocal row
        a = ws.cell(row=row, column=1, value=label)
        b = ws.cell(row=row, column=2, value=value)
        a.font = Font(bold=True, size=10)
        a.alignment = WRAP_TOP
        b.alignment = WRAP_TOP
        if link:
            b.hyperlink = link
            b.font = Font(color="1B6EC2", size=10, underline="single")
        a.border = BORDER
        b.border = BORDER
        if height:
            ws.row_dimensions[row].height = height
        row += 1

    sec("A. 표지")
    item("이름", name)
    item("상담 일시", None)
    item("상담 시간", None)
    item("희망 진로 (사전 추정)", PRE_ESTIMATE.get(name, "—"))
    item("희망 진로 (상담 확정)", None)
    item("맞춤 유형 페이지", f"{page_text} — {SITE_REPO_URL}/{page_file}",
         link=f"{SITE_REPO_URL}/{page_file}")
    item("한 줄 요약", None)

    sec("B. 1차 프로젝트 일정·커리큘럼 위치")
    item("1차 프로젝트", "2026-09-30(수) 시작 ~ 2026-10-20(화) 발표회 — 상담은 프로젝트 시작 전 진행")
    item("현재 학습 구간", "프론트엔드(HTML/CSS·React) ~ 백엔드(Python/FastAPI·DB) 학습 중")
    item("커리큘럼 순서 참고",
         "AI API·LLM 연동: 1차 프로젝트 직전 과목 / "
         "서비스 기획·요구사항 정의(PRD)·AI 기능 설계: 1차 프로젝트 이후 과목")

    sec("C. 배경 데이터")
    item("전공", r["전공"])
    item("재직 상태·현재 직무", current_status(r))
    item("희망 직무", r["희망 직무"])
    item("수강목적", r["수강목적"])

    sec("D. 지원동기·목표 (원문 — 상담 직전 읽기)")
    item("핵심 목표 (수료후)", CORE_GOAL.get(name, "—"), height=32)
    item("지원동기 (원문)", r["지원동기"], height=90)
    item("수료후목표 (원문)", r["수료후목표"], height=90)

    sec("E. 상담 전 질문·답 (레이서가 보낸 3줄 메모)",
        note="prep_guide에서 안내한 3질문 기준. 레이서가 보낸 질문·답을 상담 전에 받아 기입 (다르게 보내면 받은 대로).")
    item("질문 1 (끌리는 진로)", None, height=30)
    item("답 1", None, height=70)
    item("질문 2 (가장 큰 걱정)", None, height=30)
    item("답 2", None, height=70)
    item("질문 3 (꼭 물어볼 질문)", None, height=30)
    item("답 3", None, height=70)

    sec("F. 진로별 체크리스트·질문 가이드",
        note="상담에서 다루고 싶은 항목을 골라 옆 칸에 메모. 정리가 끝난 항목에는 ☑ 표기.")
    for gi, g in enumerate(CAREER_GUIDE[group], start=1):
        item(f"☐ {gi}", g)
    for s in SECONDARY_GUIDE.get(name, []):
        item("☐ +", s)

    sec("G. 상담 중 기록 (상담 중 직접 기입)")
    item("상담 내용", None, height=100)
    item("고민 키워드", None, height=28)
    item("액션 아이템", None, height=70)
    item("후속 조치", None, height=45)

    row += 1
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=2)
    note = ws.cell(row=row, column=1,
                   value="※ 본 시트는 상담 기록 내부용입니다. 공개 사이트(HTML)에는 레이서 개인 정보를 올리지 않습니다.")
    note.font = Font(color="73838E", italic=True, size=9)
    note.alignment = Alignment(vertical="center")


def build_log_sheet(wb, racers):
    ws = wb.create_sheet("상담 로그")
    headers = [
        "연번", "이름", "희망 진로\n(사전 추정)", "희망 진로\n(상담 확정)",
        "현재 상황", "전공", "수강목적", "핵심 목표 (수료후)",
        "상담 일시", "상담 시간", "상담 내용", "고민 키워드", "액션 아이템", "후속 조치",
    ]
    ws.append(headers)
    for i, r in enumerate(racers, start=1):
        ws.append([
            i, r["이름"], PRE_ESTIMATE.get(r["이름"], "—"), None,
            current_status(r), r["전공"], r["수강목적"], CORE_GOAL.get(r["이름"], "—"),
            None, None, None, None, None, None,
        ])
    style_sheet(ws, [5, 9, 20, 14, 16, 12, 12, 30, 12, 10, 36, 16, 30, 16])
    for idx in range(2, len(racers) + 2):
        ws.row_dimensions[idx].height = 54
    note = ws.cell(row=len(racers) + 3, column=2,
                   value="※ '상담 일시' 이후 칸은 상담 중 직접 기입. '희망 진로(상담 확정)'는 개발자/PM/창업/미확정 중 하나로.")
    note.font = Font(color="73838E", italic=True, size=10)
    note.alignment = Alignment(vertical="center")


def build_profile_sheet(wb, racers):
    ws = wb.create_sheet("레이서 프로필")
    headers = [
        "연번", "이름", "전공", "재직 상태", "현재 직무",
        "희망 직무", "수강목적", "지원동기 (원문)", "수료후목표 (원문)",
    ]
    ws.append(headers)
    for i, r in enumerate(racers, start=1):
        ws.append([
            i, r["이름"], r["전공"], r["재직 상태"], r["현재 직무"],
            r["희망 직무"], r["수강목적"], r["지원동기"], r["수료후목표"],
        ])
    style_sheet(ws, [5, 9, 12, 12, 12, 16, 12, 60, 60])
    for idx in range(2, len(racers) + 2):
        ws.row_dimensions[idx].height = 120


def main():
    racers = load_racers()
    excluded, source = load_excluded()
    skipped = [r["이름"] for r in racers if r["이름"] in excluded]
    racers = [r for r in racers if r["이름"] not in excluded]
    print(f"활동 레이서 {len(racers)}명: " + ", ".join(r["이름"] for r in racers))
    if skipped:
        print(f"제외 {len(skipped)}명 (중도탈락·수강철회): " + ", ".join(skipped) + f" [{source}]")

    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    build_log_sheet(wb, racers)
    build_profile_sheet(wb, racers)
    for i, r in enumerate(racers, start=1):
        build_individual_sheet(wb, r, i)
    os.makedirs(os.path.dirname(OUT_XLSX), exist_ok=True)
    wb.save(OUT_XLSX)
    print(f"생성 완료: {OUT_XLSX} (시트 {len(wb.sheetnames)}장: {', '.join(wb.sheetnames)})")


if __name__ == "__main__":
    main()
