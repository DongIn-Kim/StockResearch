# Platform Patch Notes

플랫폼·서버·에이전트 로직 개선 이력. 상세 내용은 여기에, CLAUDE.md에는 항목 제목만 기록.

---

## [2026-04-17] hit_limit 무한 재트리거 방지

**증상**: Claude Code가 Anthropic 5시간 쿼터 소진 시 CLI exit code 1 → 이슈 release → cron(20분) 재트리거 → 무한 루프.

**원인**: hit_limit 시 `errorCode`가 `adapter_failed`로 처리되어 에이전트가 paused되지 않고 계속 재트리거.

**수정 파일**:
- `packages/adapters/claude-local/src/server/parse.ts` — `isClaudeHitLimit()` 추가: `"You've hit your limit"` 패턴 감지
- `packages/adapters/claude-local/src/server/execute.ts` — `toAdapterResult`의 errorCode 분기에 hit_limit 감지 → `errorCode: "hit_limit"` 반환
- `server/src/services/heartbeat.ts` — `finalizeAgentStatus` 직전, hit_limit 시 에이전트를 `paused`로 전환 → cron이 paused 에이전트 건너뜀

**효과**: 토큰 소진 시 최초 1회만 중단. 에이전트는 paused 상태로 보드가 수동 재개 가능.
