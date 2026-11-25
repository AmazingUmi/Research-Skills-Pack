# -*- coding: utf-8 -*-
"""Fetch a CNIPA publication result after the user approves the terms and destination.

Use --allow-external-search with one approved keyword. Result HTML is written to
a fresh temporary directory unless EPUB_RESULT_HTML specifies an output file.
Use cnipa_epub_search.py for in-memory results; use cnipa_epub_parse.py offline.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")
from tempfile import mkdtemp
from pathlib import Path
from typing import TYPE_CHECKING, Callable
from urllib.parse import urljoin, urlsplit

if TYPE_CHECKING:
    from playwright.sync_api import Browser, BrowserContext, Page, Playwright

def _playwright():
    from playwright.sync_api import sync_playwright
    return sync_playwright()

from cnipa_epub_parse import EpubSearchHit, hits_to_jsonable, parse_search_result_html


def _ensure_utf8_stdio() -> None:
    """减轻 Windows 终端下 JSON 中文乱码（与 cnipa_epub_search.py 一致）。"""
    for stream in (sys.stdout, sys.stderr):
        try:
            if hasattr(stream, "reconfigure"):
                stream.reconfigure(encoding="utf-8", errors="replace")
        except (OSError, ValueError, TypeError):
            pass


EPUB_BASE = "https://epub.cnipa.gov.cn/"


def _require_approval(approved: bool) -> None:
    if approved is not True:
        raise PermissionError("Confirm the terms and CNIPA destination before external search.")


def _max_wait_sec() -> float:
    return float(os.environ.get("EPUB_WAF_MAX_WAIT_SEC", "180"))


def _headed() -> bool:
    return os.environ.get("PLAYWRIGHT_HEADED", "").strip() in ("1", "true", "yes")


def default_result_html_path() -> Path:
    return Path(mkdtemp(prefix="cnipa-epub-")) / "result.html"


def wait_for_epub_home_ready(page: Page, *, max_wait_sec: float | None = None) -> None:
    limit = max_wait_sec if max_wait_sec is not None else _max_wait_sec()
    page.goto(EPUB_BASE, wait_until="load", timeout=120_000)
    elapsed = 0.0
    step = 3.0
    while elapsed < limit:
        page.wait_for_timeout(int(step * 1000))
        elapsed += step
        if page.query_selector("#searchStr"):
            return
    raise TimeoutError(
        f"{limit}s 内未出现检索框 #searchStr；可增大 EPUB_WAF_MAX_WAIT_SEC 或设置 PLAYWRIGHT_HEADED=1"
    )


def _wait_result_page_settled(page: Page) -> None:
    try:
        page.wait_for_load_state("load", timeout=30_000)
    except Exception:
        pass
    try:
        page.wait_for_load_state("networkidle", timeout=25_000)
    except Exception:
        pass
    page.wait_for_timeout(800)


def _safe_page_content(page: Page, *, max_attempts: int = 10) -> str:
    last_err: Exception | None = None
    for i in range(max_attempts):
        try:
            return page.content()
        except Exception as e:
            msg = str(e).lower()
            last_err = e
            if "navigating" not in msg and "changing" not in msg:
                raise
            try:
                page.wait_for_load_state("load", timeout=20_000)
            except Exception:
                pass
            page.wait_for_timeout(400 + 200 * i)
    if last_err:
        raise last_err
    raise RuntimeError("_safe_page_content: 未返回内容")


def submit_index_search(page: Page, keyword: str, *, approved: bool = False) -> None:
    _require_approval(approved)
    page.fill("#searchStr", keyword)
    with page.expect_navigation(timeout=120_000, wait_until="load"):
        form = page.query_selector("#indexForm")
        if form:
            form.evaluate("el => el.submit()")
        else:
            page.evaluate(
                """() => {
                const f = document.getElementById('indexForm');
                if (f) f.submit();
            }"""
            )
    _wait_result_page_settled(page)


def fetch_epub_result_html(
    keyword: str,
    *,
    approved: bool = False,
    playwright_factory: Callable[[], Playwright] | None = None,
) -> str:
    """
    只拉取检索结果页 HTML，不在此函数内做正文解析。
    解析请使用 ``cnipa_epub_parse.parse_search_result_html(html)``。
    """
    _require_approval(approved)
    pw_gen = playwright_factory or _playwright
    with pw_gen() as p:
        browser = _launch_browser(p)
        context = _new_context(browser)
        try:
            page = context.new_page()
            wait_for_epub_home_ready(page)
            submit_index_search(page, keyword, approved=approved)
            return _safe_page_content(page)
        finally:
            context.close()
            browser.close()


def search_epub_keyword(
    keyword: str,
    *,
    approved: bool = False,
    playwright_factory: Callable[[], Playwright] | None = None,
) -> tuple[str, list[EpubSearchHit]]:
    html = fetch_epub_result_html(keyword, approved=approved, playwright_factory=playwright_factory)
    return html, parse_search_result_html(html)


def search_epub_keyword_with_page(
    page: Page,
    keyword: str,
    *,
    approved: bool = False,
) -> tuple[str, list[EpubSearchHit]]:
    _require_approval(approved)
    page.route("**/*", _cnipa_https_only)
    wait_for_epub_home_ready(page)
    submit_index_search(page, keyword, approved=approved)
    html = _safe_page_content(page)
    return html, parse_search_result_html(html)


def _launch_browser(p: Playwright) -> Browser:
    return p.chromium.launch(headless=not _headed(), chromium_sandbox=True)


def _cnipa_https_only(route) -> None:
    url = route.request.url
    method = route.request.method
    options = {}
    for _ in range(10):
        target = urlsplit(url)
        if target.scheme != "https" or target.netloc.lower() != "epub.cnipa.gov.cn":
            break
        # Check the next destination before a redirect can forward search terms.
        response = route.fetch(url=url, max_redirects=0, **options)
        try:
            if response.status not in (301, 302, 303, 307, 308):
                route.fulfill(response=response)
                return
            location = response.headers.get("location")
            if not location:
                break
            url = urljoin(url, location)
            if ((response.status == 303 and method != "HEAD") or
                    (response.status in (301, 302) and method == "POST")):
                method = "GET"
                options = {"method": "GET", "post_data": b""}
        finally:
            response.dispose()
    route.abort()


def _new_context(browser: Browser) -> BrowserContext:
    context = browser.new_context(locale="zh-CN", service_workers="block")
    context.route("**/*", _cnipa_https_only)
    return context


def _dump_home_debug() -> None:
    out = Path(mkdtemp(prefix="cnipa-epub-")) / "home.html"
    with _playwright() as p:
        browser = _launch_browser(p)
        context = _new_context(browser)
        page = context.new_page()
        try:
            wait_for_epub_home_ready(page)
            out.write_text(page.content(), encoding="utf-8")
            print("已保存:", out)
        finally:
            context.close()
            browser.close()


if __name__ == "__main__":
    _ensure_utf8_stdio()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-external-search", action="store_true", required=True)
    parser.add_argument("--dump-home", "-d", action="store_true")
    parser.add_argument("keyword", nargs="?")
    args = parser.parse_args()
    if args.dump_home:
        _dump_home_debug()
        sys.exit(0)
    if not args.keyword or not args.keyword.strip():
        parser.error("Supply the keyword approved for this search.")
    try:
        out_html, hits = search_epub_keyword(args.keyword, approved=args.allow_external_search)
    except Exception as e:
        print("CNIPA_EPUB_ERROR:", e, file=sys.stderr)
        sys.exit(1)
    out_path = Path(
        os.environ.get("EPUB_RESULT_HTML", "").strip() or default_result_html_path()
    )
    out_path = out_path.expanduser().resolve()
    out_path.write_text(out_html, encoding="utf-8")
    print(
        "结果页长度",
        len(out_html),
        "解析条目数",
        len(hits),
        file=sys.stderr,
        flush=True,
    )
    print("结果页 HTML 已保存:", out_path, file=sys.stderr, flush=True)
    print(
        "EPUB_HITS_JSON:",
        json.dumps(hits_to_jsonable(hits), ensure_ascii=False),
        flush=True,
    )
