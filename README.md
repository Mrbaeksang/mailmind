# MailMind — 받은 메일을 알아서 처리하는 AI 비서 에이전트

> **Google Cloud Rapid Agent Hackathon** 제출 프로젝트
> 마감: 2026-06-11 14:00 PDT (한국 6/12 새벽) · 상금 풀 $60,000 · https://rapid-agent.devpost.com/

## 한 줄
메일이 오면 에이전트가 **읽고 → 분류하고 → 요약하고 → 중요한 건 답장 초안까지** 만들어 둔다. (채팅 X, 실제로 라벨 달고 초안 쓰는 "행동하는 에이전트")

## 트랙 / 스택
- **트랙**: MongoDB (Atlas 벡터검색)
- Gmail API — 메일 읽기 / 라벨 / 초안 작성 (Google)
- Gemini — 분류·요약·할일추출·답장 초안 (Google)
- MongoDB Atlas — 메일 저장 + "그 메일 찾아줘" 벡터검색
- **MCP** — 에이전트가 Gmail/MongoDB 를 도구로 호출 (해커톤 필수 요건)
- Cloud Run — 배포 (호스팅 URL)

## 에이전트 기능 (MVP 3개)
1. 자동 분류 — 긴급 / 액션필요 / 뉴스레터 / 스팸 → Gmail 라벨
2. 요약 + 할 일 — 긴 스레드 → 3줄 요약 + 해야 할 일 추출
3. 답장 초안 — 중요 메일은 내 톤으로 초안 미리 작성 (보내진 X, draft 만)
4. (여유 시) 검색 — "지난달 그 미팅 메일" → 벡터검색

## 제출물 (Devpost)
- [ ] 호스팅된 데모 URL (Cloud Run)
- [ ] 공개 오픈소스 repo + OSI 라이선스 (MIT/Apache)
- [ ] 텍스트 설명 (기능·기술·데이터소스·배운 점)
- [ ] ~3분 데모 영상 (vstudio 로 제작)

## 12일 일정
| 일 | 작업 |
|---|---|
| D1~2 | Gmail API + Gemini 연결 (읽고 분류만) |
| D3~5 | MongoDB 저장 + 벡터검색 + MCP 래핑 |
| D6~8 | 요약·할일·답장초안 + 간단 웹UI |
| D9~10 | Cloud Run 배포 + repo 정리 |
| D11 | 데모영상 + Devpost 작성 |
| D12 새벽 | 제출 |

## ⚠️ 주의
- **본인 진짜 메일 X** — 데모는 테스트 Gmail 계정 + 샘플 메일 (프라이버시 + 심사자가 돌려봐야 함)
- Google Cloud $100 크레딧: 6/4까지 신청 (https://forms.gle/xfv9vQzfRfNCCVbG7)
- 회사 코드 재활용 금지 (오픈소스 신규 작성)

## 개발 (Development)

```bash
uv sync                         # 의존성 설치
uv run pytest                   # 테스트 (현재 core 6개 모듈, 19 tests)
uv run ruff check . && uv run ruff format .   # 린트 + 포맷
cp .env.example .env            # 비밀값 채우기 (실제 .env 는 커밋 금지)
```

**현재 구현 상태**: 순수 로직 코어가 TDD로 완성됨 (`src/mailmind/core/`):
`email_parsing` · `embedding_input` · `ingest_transform` · `classifier` · `summarizer` · `draft_writer`.
LLM/임베딩은 `mailmind.ports` 의 좁은 포트(`TextModel`/`EmbeddingModel`) 뒤에 있어 코어는 I/O 없이 테스트됨.

**다음 작업**: 어댑터(Vertex·Gmail/Mongo 공식 MCP)·에이전트 결선·웹·배포 — GitHub 이슈 [#2~#10](https://github.com/Mrbaeksang/mailmind/issues) 참조 (PRD = [#1](https://github.com/Mrbaeksang/mailmind/issues/1)). 이들은 외부 계정(GCP·Atlas·테스트 Gmail+Developer Preview)이 선행 필요 → 이슈 #2(S0)가 그 셋업·검증 슬라이스.

## 라이선스
MIT — `LICENSE` 참조. (OSI 승인 라이선스, 해커블 제출 요건 충족)
