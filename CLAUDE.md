# MailMind

받은 메일을 읽고 → 분류·요약·할일추출 → 답장 초안까지 만들어 두는 **행동형 이메일 에이전트**.
질문에 답만 하는 챗봇이 아니라 Gmail 라벨을 달고 초안을 쓰는 등 **실제 동작**을 한다.
컨텍스트: Google Cloud Rapid Agent Hackathon 제출작 (마감 2026-06-11). 상세는 @README.md.

## 📍 세션 시작 시 (먼저 이거)
새 세션을 열면 **아래 "현재 상태"를 보고, 미완료 항목을 사용자에게 한 줄로 브리핑**한 뒤 다음 할 일을 제안한다. 코드가 아직이면 셋업부터, 셋업 끝났으면 다음 수직 슬라이스부터.

## 현재 상태 / 다음 할 일 (수시 갱신)
- [x] 프로젝트 폴더 + git + CLAUDE/README 셋업
- [x] GCP $100 크레딧 신청 폼 제출 (2026-05-30)
- [ ] **GCP 코드 도착(≤5영업일) → console.cloud.google.com/billing/redeem 에서 redeem ⏰ 6/4 전 필수**
- [ ] GCP 계정 + **billing account 생성** (redeem 선행조건)
- [x] Devpost 해커톤 **Join** + 제출 draft 시작 (name/pitch 입력, 2026-05-30)
- [ ] MongoDB Atlas 무료 M0 클러스터 + 벡터검색
- [ ] 테스트 Gmail 계정 + 샘플 메일 + Gmail API OAuth (⚠️ 진짜 메일 X)
- [x] PRD(이슈 #1) + 슬라이스 이슈 #2~#10 발행 (S0/S8=ready-for-human)
- [x] **백엔드 TDD 완성** (43 tests green, ruff clean, 계정없이 fakes/mongomock/TestClient 검증): core 6개 + store(+$vectorSearch 빌더) + ingest + mcp 정책(send/파괴툴 차단) + web(FastAPI) + operations(process_inbox/semantic_search)
- [ ] 모델: **Gemini 3.5 Flash**(생성) + **Gemini Embedding 2**(임베딩, 3072) — 배선 시 정확한 API id 확인
- [ ] **남음(계정 필요)**: 라이브 어댑터(Vertex·Gmail/Mongo MCP 실연결)·ADK 에이전트·Next UI·샘플생성·배포 → 이슈 #2(S0) 선행
- [ ] **이슈 #2 (S0)**: 외부계정 셋업 + Gmail/Mongo 공식 MCP 실접속 검증 (사용자 선행 필요) → 이후 어댑터·에이전트·웹·배포(이슈 #3~#10)
- [ ] 슬라이스2: MongoDB 적재 + 벡터검색 + MCP 래핑
- [ ] 슬라이스3: 요약·할일·답장초안 + 웹UI
- [ ] 배포(Cloud Run) → 데모영상(vstudio) → Devpost 제출

> 항목 끝낼 때마다 이 체크리스트 갱신. 셋업 4개(GCP·Devpost·Atlas·Gmail)는 사용자가 직접(계정/비번), 코딩은 여기서.

## Stack
- **Python 3.11** · agent = Google Agent Builder + Gemini, 도구 호출 = **MCP**
- Gmail API (읽기/라벨/draft) · MongoDB Atlas (저장 + 벡터검색) · Cloud Run (배포)
- 패키지: `uv` (requirements 는 `pyproject.toml`)

## Commands
```bash
uv sync                      # 의존성 설치
uv run mailmind ingest       # Gmail → MongoDB 적재 (테스트 계정만)
uv run mailmind run          # 에이전트 1회 처리 (분류·요약·초안)
uv run mailmind serve        # 로컬 웹 UI / API (포트 8000)
uv run pytest                # 테스트
uv run ruff check . && uv run ruff format .   # 린트+포맷
```
> 위 entrypoint 는 구현하며 채운다. 새 명령 추가 시 이 표를 갱신.

## Structure
- `src/mailmind/agent/` — 에이전트 루프 + 도구 정의
- `src/mailmind/mcp/` — Gmail · MongoDB 를 감싼 MCP 서버
- `src/mailmind/core/` — 분류·요약·초안 로직 (Gemini 프롬프트)
- `scripts/` — 셋업·배포 헬퍼 · `docs/` — 설계 노트/ADR

## Conventions
- 작은 수직 슬라이스로 작업. 기능 1개 = 테스트 먼저(red-green-refactor).
- 함수는 작고 단일 책임. 모듈 경계 = `agent / mcp / core` 분리 유지.
- 타입힌트 필수. 에러는 삼키지 말고 로깅 후 전파.
- 비밀값은 `.env` 만 (커밋 금지 — `.gitignore` 확인). 코드에 키 하드코딩 X.

## 🔒 절대 규칙 (해커톤 + 안전)
- **실제 개인 메일 금지.** 데모·개발은 **전용 테스트 Gmail 계정 + 샘플 메일**만. 진짜 받은편지함 연결 X.
- **메일 자동 발송 X.** 답장은 **draft(초안)까지만** 생성. 사람이 검토 후 보냄.
- **오픈소스 제출**: repo 공개 + OSI 라이선스(**MIT**, `LICENSE`). 회사 코드 재활용 금지 — 전부 신규 작성.
- Google Cloud / MongoDB 외 **경쟁 서비스(AWS 등) 사용 금지** (트랙 규칙).

## Agent skills

### Issue tracker
Issues are tracked in **GitHub Issues** (`gh` CLI). See `docs/agents/issue-tracker.md`.

### Triage labels
Default label vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs
Single-context (`CONTEXT.md` + `docs/adr/` at repo root). See `docs/agents/domain.md`.

## References
- 프로젝트 계획·일정·제출물 체크리스트 → @README.md
- 해커톤 규칙 → https://rapid-agent.devpost.com/rules
- 워크스테이션 환경 → `~/CLAUDE.md`
