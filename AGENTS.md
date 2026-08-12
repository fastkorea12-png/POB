# POB 성경클럽 — 에이전트 컨텍스트

## 프로젝트 정의

POB는 BibleTree 주간 원천(커리큘럼·본문표·공과가이드·설교·PPT)을
**70분 어린이 예배·성경 내러티브·질문·공동체 활동**으로 재구성하는 실행 체계다.

단순 HTML 변환 도구가 아니다. 본문이 살아나고, 아이들이 참여하며,
은혜가 가정까지 이어지도록 BibleTree 원천의 구속사적 흐름을
현장에서 실행 가능한 형태로 재구성한다.

대상: 초등부 혼합반 (저학년·고학년 함께, 교사 1명 + 기기 1대)
운영: 주일 70분 완결 구조

---

## 정본 식별자

**수업은 날짜(date) + 본문(passage)으로 식별한다.**
월 주차 번호, lesson_number, 파일 순번은 참조용이며 식별자가 아니다.

> 이유: BibleTree 커리큘럼이 매달 조정되고, 절기 주간에 순번이 바뀔 수 있다.
> 날짜와 본문이 일치해야만 같은 수업이다.

---

## 70분 예배 구조 (고정)

| 순서 | 이름 | 시간 | 내용 |
|---|---|---|---|
| 1 | 도입 | 3분 | 오늘의 주제·본문 소개, 아이들 집중 |
| 2 | 찬양·기도 | 7분 | 찬양 1곡 + 기도 |
| 3 | Book | 8분 | 성경 본문 읽기 + 내러티브 (Q1) |
| 4 | Look | 7분 | 교훈 발견 + 내면 성찰 (Q2) |
| 5 | Took | 5분 | 이번 주 실천 결단 (Q3) |
| 6 | Games | 20분 | 공동체 활동 (본문 연결 게임·움직임) |
| 7 | 암송 | 10분 | 주간 암송 구절 |
| 8 | 마무리 | 10분 | 기도·가정 연계 안내 |
| | **합계** | **70분** | |

---

## BibleTree 원천 경로

```
/Users/kimchoongman/AI 로컬/BibleTree_HEM/
├── sep_oct_curriculum.md     ← 9-10월 주차별 주제·설교 본문 (정본)
├── sep_oct_passages.md       ← 날짜별 본문 상세 (정본)
├── sep_oct/weekly/           ← 날짜별 묵상 JSON (4개 연령)
├── lessons/                  ← 주차별 공과가이드 .md
├── sermons/                  ← 주차별 설교문 .md
└── outputs/presentations/    ← 저학년 PPT .pptx
```

---

## 소스 충돌 처리 원칙

원천 파일 사이에 날짜·본문·제목이 불일치하면 **즉시 blocked 처리**한다.
임의로 어느 쪽이 맞는지 판단하거나 수정하지 않는다.

**알려진 충돌 (해결 전 blocked 상태 유지)**
- `2026-08-16` / 섬김으로 복음을 전하다:
  - `jul_aug_curriculum.md` → `야고보서 1:2-10`
  - 이전 기록 일부 → `야고보서 1:1-8`
  - → 사람 확인 후 정본 확정 전까지 이 날짜 수업 생성 금지

---

## 미디어 생성 승인 원칙

Gemini 영상·이미지, HeyGen 영상 등 **비용이 발생하는 미디어는
사람의 명시적 승인 없이 생성하지 않는다.**

승인 전 단계: 프롬프트 초안만 `scripts/gemini_prompts/[slug].json`에 저장.
승인 후: `review.media_approved = true` 확인 후에만 API 호출 실행.

영상 길이·컷 수는 내용에 따라 결정한다. Q4 10초 고정 제거.

---

## 초등부 혼합반 질문 원칙

각 Q(Book·Look·Took)에 **기본 질문(저학년)과 확장 질문(고학년)** 두 세트를 준비한다.
교사가 현장에서 선택하거나 순서대로 병행할 수 있도록 한다.

---

## 4-에이전트 역할 분담

| 에이전트 | 역할 | 소유 | 금지 |
|---|---|---|---|
| **Codex** | 원천 파싱 → lesson-data.json, 미디어 프롬프트 준비, 주간 자동화 | `data/`, `scripts/` | HTML 편집, 미디어 API 직접 호출 |
| **Gemini** | 승인 후 영상·이미지 생성 | `assets/` (생성물) | 미승인 실행 |
| **Claude 대화** | 신학·목회 검토, 조율, 보고 | 읽기 전용 | 파일 직접 생성 |
| **Claude Code** | lesson-XX.html 조립, GitHub 배포 | `lesson-*.html` | 미승인 푸시, BibleTree 수정 |

---

## 승인 게이트 (사람만 변경 가능)

| 게이트 | 조건 | 이후 가능 작업 |
|---|---|---|
| `source_verified` | 날짜+본문 충돌 없음 확인 | lesson-data.json 완성 |
| `content_approved` | 신학·목회 검토 완료 | 미디어 프롬프트 확정 |
| `media_approved` | 비용 발생 미디어 생성 동의 | Gemini/HeyGen API 호출 |
| `html_approved` | HTML 완성본 확인 | GitHub 배포 |

`review.status` 값: `draft` → `source_conflict` (blocked) → `reviewed` → `approved` → `deployed`

---

## 금지 사항

- BibleTree 원본 파일 수정 금지
- `lesson-*.html`, `index.html`, `detail.html` 직접 편집 금지
- 승인(`html_approved`) 없이 GitHub 푸시 금지
- 학생 개인정보를 어떤 파일에도 포함 금지
- 월 주차 번호·lesson_number를 식별자로 사용 금지
- 미디어 비용 발생 작업을 승인 없이 실행 금지
- 원천 충돌 시 임의 판단 금지 — 반드시 blocked 처리 후 보고
