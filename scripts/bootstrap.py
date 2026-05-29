#!/usr/bin/env python3
"""
SR Research Centre — Bootstrap Script
클론 후 최초 1회 실행하여 회사·에이전트를 자동 생성합니다.

사용법: python3 scripts/bootstrap.py
"""

import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path


# ─────────────────────────────────────────────
# 1. .env 확인 및 로드
# ─────────────────────────────────────────────

def find_project_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("❌ git 리포지토리가 아닙니다. 프로젝트 루트에서 실행하세요.")
        sys.exit(1)
    return Path(result.stdout.strip())


def load_env(env_path: Path) -> dict:
    env = {}
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                env[key.strip()] = value.strip()
    return env


def update_env_file(env_path: Path, updates: dict) -> None:
    """기존 .env 파일에서 키를 교체하거나 없으면 추가합니다."""
    lines = env_path.read_text(encoding="utf-8").splitlines()
    updated_keys = set()

    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and "=" in stripped:
            key = stripped.split("=", 1)[0].strip()
            if key in updates:
                new_lines.append(f"{key}={updates[key]}")
                updated_keys.add(key)
                continue
        new_lines.append(line)

    # 기존에 없던 키 추가
    for key, value in updates.items():
        if key not in updated_keys:
            new_lines.append(f"{key}={value}")

    env_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


PROJECT_ROOT = find_project_root()
ENV_PATH = PROJECT_ROOT / ".env"
ENV_EXAMPLE_PATH = PROJECT_ROOT / ".env.example"

print("🚀 SR Research Centre Bootstrap 시작")
print(f"   프로젝트 루트: {PROJECT_ROOT}")

if not ENV_PATH.exists():
    if ENV_EXAMPLE_PATH.exists():
        shutil.copy(ENV_EXAMPLE_PATH, ENV_PATH)
        print()
        print("📋 .env.example을 .env로 복사했습니다.")
        print("   ⚠️  .env 파일을 열어 아래 항목을 직접 입력하세요:")
        print("      - PAPERCLIP_AGENT_JWT_SECRET (openssl rand -base64 32)")
        print("      - DART_API_KEY, ECOS_API_KEY, FRED_API_KEY (선택)")
        print("   완료 후 다시 실행하세요: python3 scripts/bootstrap.py")
    else:
        print("❌ .env.example 파일을 찾을 수 없습니다.")
    sys.exit(0)

env = load_env(ENV_PATH)
os.environ.update(env)

# PAPERCLIP_AGENT_JWT_SECRET 필수 확인
jwt_secret = env.get("PAPERCLIP_AGENT_JWT_SECRET", "")
if not jwt_secret or jwt_secret in ("YOUR_JWT_SECRET_HERE", ""):
    print()
    print("❌ .env 파일에 PAPERCLIP_AGENT_JWT_SECRET이 설정되지 않았습니다.")
    print("   openssl rand -base64 32 로 생성 후 .env에 입력하세요.")
    sys.exit(1)

print("✅ .env 로드 완료")


# ─────────────────────────────────────────────
# 2. 서버 상태 확인
# ─────────────────────────────────────────────

BASE_URL = "http://127.0.0.1:3100"
AUTH_HEADER = "Bearer local-board"


def api_get(path: str) -> dict | list:
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url, headers={"Authorization": AUTH_HEADER})
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.loads(resp.read().decode())


def api_post(path: str, body: dict) -> dict:
    url = f"{BASE_URL}{path}"
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Authorization": AUTH_HEADER,
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode())


def api_patch(path: str, body: dict) -> dict:
    url = f"{BASE_URL}{path}"
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="PATCH",
        headers={
            "Authorization": AUTH_HEADER,
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode())


print("🔍 서버 상태 확인 중...")
try:
    health_url = f"{BASE_URL}/api/health"
    req = urllib.request.Request(health_url)
    with urllib.request.urlopen(req, timeout=5) as resp:
        pass
    print("✅ 서버 정상 응답")
except Exception:
    print()
    print("❌ 서버에 연결할 수 없습니다.")
    print("   pnpm dev 를 먼저 실행한 후 다시 시도하세요.")
    sys.exit(1)


# ─────────────────────────────────────────────
# 3. 회사 조회 또는 생성
# ─────────────────────────────────────────────

print("🏢 회사 정보 확인 중...")
try:
    companies = api_get("/api/companies")
except Exception as e:
    print(f"❌ 회사 목록 조회 실패: {e}")
    sys.exit(1)

if companies:
    company = companies[0]
    company_id = company["id"]
    print(f"✅ 기존 회사 사용: {company.get('name', '')} ({company_id})")
else:
    print("   기존 회사 없음 → SR Research Centre 생성 중...")
    try:
        company = api_post("/api/companies", {
            "name": "SR Research Centre",
            "issuePrefix": "SRR",
        })
        company_id = company["id"]
        print(f"✅ 회사 생성 완료: {company_id}")
    except Exception as e:
        print(f"❌ 회사 생성 실패: {e}")
        sys.exit(1)

# .env 업데이트
update_env_file(ENV_PATH, {"SR_COMPANY_ID": company_id})
print(f"📝 .env → SR_COMPANY_ID={company_id}")


# ─────────────────────────────────────────────
# 4. 에이전트 조회 또는 생성
# ─────────────────────────────────────────────

AGENTS = [
    ("Head of Research",     "ceo",        "SR_HEAD_OF_RESEARCH_ID"),
    ("Macro Analyst",        "researcher", "SR_MACRO_ANALYST_ID"),
    ("Quant Analyst",        "researcher", "SR_QUANT_ANALYST_ID"),
    ("Report Writer",        "general",    "SR_REPORT_WRITER_ID"),
    ("Review Analyst",       "qa",         "SR_REVIEW_ANALYST_ID"),
    ("IT Support",           "general",    "SR_IT_SUPPORT_ID"),
    ("Sector Analyst",       "researcher", "SR_SECTOR_ANALYST_ID"),
    ("Market Analyst",       "researcher", "SR_MARKET_ANALYST_ID"),
    ("Tech Analyst",         "researcher", "SR_TECH_ANALYST_ID"),
    ("Policy & ESG Analyst", "researcher", "SR_POLICY_ESG_ANALYST_ID"),
    ("Company Analyst",      "researcher", "SR_COMPANY_ANALYST_ID"),
    ("Business Analyst",     "researcher", "SR_BUSINESS_ANALYST_ID"),
    ("Finance Analyst",      "researcher", "SR_FINANCE_ANALYST_ID"),
    ("Principal Investigator","researcher","SR_PRINCIPAL_INVESTIGATOR_ID"),
    ("Econometrician",       "researcher", "SR_ECONOMETRICIAN_ID"),
    ("Financial Engineer",   "researcher", "SR_FINANCIAL_ENGINEER_ID"),
    ("Research Associate",   "general",    "SR_RESEARCH_ASSOCIATE_ID"),
    ("Scientific Reviewer",  "qa",         "SR_SCIENTIFIC_REVIEWER_ID"),
]

print(f"\n👥 에이전트 확인 중 (총 {len(AGENTS)}명)...")

# 기존 에이전트 목록 조회
try:
    existing_agents = api_get(f"/api/companies/{company_id}/agents")
    existing_by_name = {a["name"]: a["id"] for a in existing_agents}
except Exception as e:
    print(f"❌ 에이전트 목록 조회 실패: {e}")
    sys.exit(1)

agent_ids: dict[str, str] = {}
env_updates: dict[str, str] = {}
created_count = 0
reused_count = 0

for name, role, env_key in AGENTS:
    if name in existing_by_name:
        agent_id = existing_by_name[name]
        agent_ids[name] = agent_id
        env_updates[env_key] = agent_id
        print(f"   ♻️  재사용: {name} ({agent_id[:8]}...)")
        reused_count += 1
    else:
        try:
            agent = api_post(f"/api/companies/{company_id}/agents", {
                "name": name,
                "role": role,
            })
            agent_id = agent["id"]
            agent_ids[name] = agent_id
            env_updates[env_key] = agent_id
            print(f"   ✨ 생성: {name} ({agent_id[:8]}...)")
            created_count += 1
        except Exception as e:
            print(f"   ❌ 생성 실패: {name} — {e}")

# .env 업데이트
update_env_file(ENV_PATH, env_updates)
print(f"\n📝 .env → 에이전트 ID {len(env_updates)}개 업데이트 완료")


# ─────────────────────────────────────────────
# 5. 커맨드 파일 및 CLAUDE.md 패치
# ─────────────────────────────────────────────

head_id = agent_ids.get("Head of Research", "")
pi_id = agent_ids.get("Principal Investigator", "")
it_id = agent_ids.get("IT Support", "")
project_root_str = str(PROJECT_ROOT)

patched_files: list[str] = []

COMMAND_FILES = [
    PROJECT_ROOT / ".claude" / "commands" / "academic_paper.md",
    PROJECT_ROOT / ".claude" / "commands" / "company_analysis.md",
    PROJECT_ROOT / ".claude" / "commands" / "sector_analysis.md",
]

REPLACEMENTS_COMMANDS = [
    ("YOUR_HEAD_OF_RESEARCH_AGENT_ID", head_id),
    ("YOUR_PRINCIPAL_INVESTIGATOR_AGENT_ID", pi_id),
    ("{PROJECT_ROOT}", project_root_str),
]

print("\n📄 커맨드 파일 패치 중...")
for cmd_file in COMMAND_FILES:
    if not cmd_file.exists():
        print(f"   ⚠️  파일 없음 (건너뜀): {cmd_file}")
        continue
    content = cmd_file.read_text(encoding="utf-8")
    changed = False
    for old, new in REPLACEMENTS_COMMANDS:
        if old in content and new:
            content = content.replace(old, new)
            changed = True
    if changed:
        cmd_file.write_text(content, encoding="utf-8")
        rel = cmd_file.relative_to(PROJECT_ROOT)
        print(f"   ✅ 패치: {rel}")
        patched_files.append(str(rel))
    else:
        rel = cmd_file.relative_to(PROJECT_ROOT)
        print(f"   ➖ 변경 없음: {rel}")

# CLAUDE.md 패치
print("\n📄 CLAUDE.md 패치 중...")
claude_md = PROJECT_ROOT / "CLAUDE.md"
if claude_md.exists():
    content = claude_md.read_text(encoding="utf-8")
    changed = False
    for old, new in [
        ("YOUR_IT_SUPPORT_AGENT_ID", it_id),
        ("{PROJECT_ROOT}", project_root_str),
    ]:
        if old in content and new:
            content = content.replace(old, new)
            changed = True
    if changed:
        claude_md.write_text(content, encoding="utf-8")
        print("   ✅ 패치: CLAUDE.md")
        patched_files.append("CLAUDE.md")
    else:
        print("   ➖ 변경 없음: CLAUDE.md")
else:
    print("   ⚠️  CLAUDE.md 없음 (건너뜀)")


# ─────────────────────────────────────────────
# 6. 완료 보고
# ─────────────────────────────────────────────

print()
print("=" * 60)
print("🎉 Bootstrap 완료!")
print(f"   회사 ID : {company_id}")
print(f"   에이전트: 신규 {created_count}명 / 재사용 {reused_count}명")
if patched_files:
    print(f"   패치 파일:")
    for f in patched_files:
        print(f"      - {f}")
print()
print("다음 단계:")
print("  1. pnpm dev 로 서버 실행")
print("  2. http://127.0.0.1:3100 에서 플랫폼 확인")
print("  3. INFRA.md 에서 API 키 설정 확인")
print("=" * 60)
