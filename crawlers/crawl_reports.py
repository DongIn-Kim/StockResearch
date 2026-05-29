"""
리서치 리포트 크롤러 — 네이버 금융 리서치
출처: https://finance.naver.com/research/

사용법:
    python crawl_reports.py sector   --pages 3 --keyword 금융
    python crawl_reports.py company  --pages 3 --keyword 은행
    python crawl_reports.py both     --pages 5
"""

import argparse
import re
import time
from datetime import date
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin

import requests
import pdfplumber
from bs4 import BeautifulSoup
from tqdm import tqdm

# ── 경로 설정 ──────────────────────────────────────────────────────────────
BASE_DIR = Path("/Users/pc/Documents/sr_research_centre/workspace/references")
SECTOR_DIR = BASE_DIR / "sector-reports"
COMPANY_DIR = BASE_DIR / "company-reports"
SOURCES_FILE = Path("/Users/pc/Documents/sr_research_centre/workspace/sources.md")

NAVER_BASE = "https://finance.naver.com"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Referer": "https://finance.naver.com/research/",
    "Accept-Language": "ko-KR,ko;q=0.9",
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)

# ── HTML 파싱 ───────────────────────────────────────────────────────────────

def fetch(url: str, retries: int = 3) -> Optional[BeautifulSoup]:
    for attempt in range(retries):
        try:
            resp = SESSION.get(url, timeout=15)
            resp.raise_for_status()
            resp.encoding = "euc-kr"
            return BeautifulSoup(resp.text, "lxml")
        except requests.RequestException as e:
            print(f"  [재시도 {attempt+1}/{retries}] {url} — {e}")
            time.sleep(2 ** attempt)
    return None


def _extract_pdf_url(td) -> Optional[str]:
    """td 태그에서 PDF 절대 URL 추출"""
    a = td.select_one("a[href]")
    if a:
        href = a["href"]
        if href.startswith("http"):
            return href
        return urljoin(NAVER_BASE, href)
    return None


def parse_sector_list(page: int) -> list[dict]:
    """산업분석 목록 파싱 — 한 페이지
    컬럼: [0]섹터 | [1]제목+링크 | [2]증권사 | [3]PDF링크 | [4]날짜 | [5]조회수
    """
    url = f"{NAVER_BASE}/research/industry_list.naver?page={page}"
    soup = fetch(url)
    if not soup:
        return []

    rows = []
    table = soup.select_one("table.type_1")
    if not table:
        return []

    for tr in table.select("tr"):
        tds = tr.select("td")
        if len(tds) < 6:
            continue
        title_a = tds[1].select_one("a")
        if not title_a:
            continue

        rows.append({
            "type": "sector",
            "sector": tds[0].get_text(strip=True),
            "title": title_a.get_text(strip=True),
            "detail_url": urljoin(NAVER_BASE + "/research/", title_a["href"]),
            "firm": tds[2].get_text(strip=True),
            "pdf_url": _extract_pdf_url(tds[3]),
            "date": tds[4].get_text(strip=True),
        })
    return rows


def parse_company_list(page: int) -> list[dict]:
    """기업분석 목록 파싱 — 한 페이지
    컬럼: [0]종목+링크 | [1]제목+링크 | [2]증권사 | [3]PDF링크 | [4]날짜 | [5]조회수
    """
    url = f"{NAVER_BASE}/research/company_list.naver?page={page}"
    soup = fetch(url)
    if not soup:
        return []

    rows = []
    table = soup.select_one("table.type_1")
    if not table:
        return []

    for tr in table.select("tr"):
        tds = tr.select("td")
        if len(tds) < 6:
            continue
        title_a = tds[1].select_one("a")
        if not title_a:
            continue

        ticker_a = tds[0].select_one("a")
        rows.append({
            "type": "company",
            "ticker_name": tds[0].get_text(strip=True),
            "title": title_a.get_text(strip=True),
            "detail_url": urljoin(NAVER_BASE + "/research/", title_a["href"]),
            "firm": tds[2].get_text(strip=True),
            "pdf_url": _extract_pdf_url(tds[3]),
            "date": tds[4].get_text(strip=True),
            "sector": "",
        })
    return rows


def resolve_pdf_url(detail_url: str) -> Optional[str]:
    """상세 페이지에서 실제 PDF URL 추출"""
    soup = fetch(detail_url)
    if not soup:
        return None
    a = soup.select_one("a[href*='.pdf']") or soup.select_one("a[href*='research/pdf']")
    if a:
        return urljoin(NAVER_BASE, a["href"])
    return None

# ── PDF 다운로드 & 텍스트 추출 ───────────────────────────────────────────────

def sanitize(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "_", name).strip()


def download_pdf(pdf_url: str, dest_path: Path) -> bool:
    if dest_path.exists():
        return True
    try:
        resp = SESSION.get(pdf_url, timeout=30, stream=True)
        resp.raise_for_status()
        dest_path.write_bytes(resp.content)
        return True
    except requests.RequestException as e:
        print(f"  [PDF 다운로드 실패] {pdf_url} — {e}")
        return False


def pdf_to_text(pdf_path: Path) -> str:
    try:
        with pdfplumber.open(pdf_path) as pdf:
            pages = []
            for p in pdf.pages[:30]:   # 최대 30페이지
                text = p.extract_text()
                if text:
                    pages.append(text)
            return "\n\n".join(pages)
    except Exception as e:
        print(f"  [PDF 파싱 실패] {pdf_path.name} — {e}")
        return ""

# ── 저장 ───────────────────────────────────────────────────────────────────

def save_report(item: dict, text: str, out_dir: Path) -> Optional[Path]:
    """텍스트를 Markdown으로 저장"""
    today = date.today().isoformat()
    safe_title = sanitize(item["title"])[:60]
    firm = sanitize(item.get("firm", "unknown"))
    filename = f"{today}_{firm}_{safe_title}.md"
    dest = out_dir / filename

    meta_lines = [
        "---",
        f"source: 네이버금융 리서치 — {item.get('firm', '')}",
        f"url: {item.get('pdf_url') or item.get('detail_url', '')}",
        f"retrieved: {today}",
        f"type: {item['type']}",
        f"sector: {item.get('sector', '')}",
        f"title: {item['title']}",
        "---",
        "",
        f"# {item['title']}",
        f"> 발행사: {item.get('firm', '')}  |  날짜: {item.get('date', '')}",
        "",
    ]
    dest.write_text("\n".join(meta_lines) + "\n" + text, encoding="utf-8")
    return dest


def append_sources_md(items: list[dict]):
    """sources.md 레지스트리 업데이트"""
    today = date.today().isoformat()
    lines = [f"\n## 크롤링 배치 — {today}\n"]
    for it in items:
        lines.append(
            f"- [{it['title']}]({it.get('pdf_url') or it.get('detail_url', '')}) "
            f"| {it.get('firm', '')} | {it.get('sector', '')} | {it.get('date', '')}"
        )
    with SOURCES_FILE.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

# ── 메인 파이프라인 ──────────────────────────────────────────────────────────

def collect(report_type: str, pages: int, keyword: Optional[str]) -> list[dict]:
    items = []
    for page in range(1, pages + 1):
        if report_type == "sector":
            batch = parse_sector_list(page)
        else:
            batch = parse_company_list(page)

        if keyword:
            batch = [
                it for it in batch
                if keyword in it["title"] or keyword in it.get("sector", "")
            ]
        items.extend(batch)
        time.sleep(0.8)
    return items


def run(report_type: str, pages: int, keyword: Optional[str], max_items: int):
    types = ["sector", "company"] if report_type == "both" else [report_type]
    all_saved: list[dict] = []

    for rtype in types:
        out_dir = SECTOR_DIR if rtype == "sector" else COMPANY_DIR
        out_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n{'산업분석' if rtype == 'sector' else '기업분석'} 목록 수집 중 ({pages}페이지) ...")
        items = collect(rtype, pages, keyword)
        items = items[:max_items]
        print(f"  → {len(items)}건 발견")

        for item in tqdm(items, desc="다운로드 & 변환"):
            # PDF URL 없으면 상세 페이지에서 추출 시도
            if not item.get("pdf_url"):
                item["pdf_url"] = resolve_pdf_url(item["detail_url"])
                time.sleep(0.5)

            if not item.get("pdf_url"):
                print(f"  [SKIP — PDF 없음] {item['title']}")
                continue

            # 파일명
            today = date.today().isoformat()
            safe = sanitize(item["title"])[:50]
            firm = sanitize(item.get("firm", "unknown"))
            pdf_path = out_dir / f"{today}_{firm}_{safe}.pdf"

            ok = download_pdf(item["pdf_url"], pdf_path)
            time.sleep(0.6)

            if ok:
                text = pdf_to_text(pdf_path)
                saved = save_report(item, text, out_dir)
                if saved:
                    all_saved.append(item)
                    print(f"  [OK] {saved.name}")

    if all_saved:
        append_sources_md(all_saved)
        print(f"\n완료: {len(all_saved)}건 저장 → {BASE_DIR}")
        print(f"sources.md 업데이트: {SOURCES_FILE}")
    else:
        print("\n저장된 리포트 없음. PDF URL을 찾지 못했거나 필터 결과 없음.")


# ── CLI ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="네이버 금융 리서치 리포트 크롤러")
    parser.add_argument(
        "type",
        choices=["sector", "company", "both"],
        help="수집 대상: sector(산업분석) | company(기업분석) | both",
    )
    parser.add_argument("--pages", type=int, default=3, help="수집 페이지 수 (기본 3)")
    parser.add_argument("--keyword", type=str, default=None, help="제목/섹터 필터 키워드 (예: 금융, 은행)")
    parser.add_argument("--max", type=int, default=30, help="최대 수집 건수 (기본 30)")
    args = parser.parse_args()

    print(f"[크롤러 시작] type={args.type} | pages={args.pages} | keyword={args.keyword} | max={args.max}")
    run(args.type, args.pages, args.keyword, args.max)


if __name__ == "__main__":
    main()
