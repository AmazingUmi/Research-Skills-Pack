from pathlib import Path
import sys
from unittest.mock import Mock

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(SCRIPTS / "disclosure"))
import cnipa_epub_crawler as crawler
import cnipa_epub_search as search
from render_flowchart_svg import claim_step_map


def test_external_search_requires_approval_before_browser_start():
    factory = Mock()
    with pytest.raises(PermissionError):
        crawler.fetch_epub_result_html("query", playwright_factory=factory)
    factory.assert_not_called()
    assert search.main(["query"]) != 0


def test_navigation_policy_and_temp_paths():
    assert crawler.EPUB_BASE.startswith("https://")
    assert not crawler.default_result_html_path().is_relative_to(SCRIPTS)
    route = Mock()
    route.request.url = "http://epub.cnipa.gov.cn/"
    crawler._cnipa_https_only(route)
    route.abort.assert_called_once()
    route.fetch.assert_not_called()
    route = Mock()
    route.request.url = crawler.EPUB_BASE
    route.fetch.return_value.status = 302
    route.fetch.return_value.headers = {"location": "http://epub.cnipa.gov.cn/result"}
    crawler._cnipa_https_only(route)
    route.fetch.assert_called_once_with(url=crawler.EPUB_BASE, max_redirects=0)
    route.abort.assert_called_once()


def test_same_origin_prg_redirect_preserves_encrypted_search():
    route = Mock()
    route.request.url, route.request.method = crawler.EPUB_BASE, "POST"
    redirect = Mock(status=303, headers={"location": "/result"})
    result = Mock(status=200)
    route.fetch.side_effect = [redirect, result]
    crawler._cnipa_https_only(route)
    route.fulfill.assert_called_once_with(response=result)
    assert route.fetch.call_args_list[-1].kwargs == {
        "url": crawler.EPUB_BASE + "result", "method": "GET", "post_data": b"", "max_redirects": 0}


def test_chinese_adjacent_steps():
    assert claim_step_map([{"number": 1, "text": "包括步骤S1采集，再执行S2，XS3不表示步骤。"}]) == {1: {"S1", "S2"}}


def test_multiline_display_formula_keeps_natural_size(tmp_path):
    from docx import Document
    from PIL import Image
    from md_to_docx import _embed_from_image_ref

    name = "formula.png"
    Image.new("RGB", (400, 200), "white").save(tmp_path / name, dpi=(200, 200))
    doc = Document()
    _embed_from_image_ref("块公式", name, tmp_path, doc=doc)
    actual = doc.inline_shapes[0]
    assert actual.height.inches == pytest.approx(1.0, rel=0.02)
    assert actual.width.inches == pytest.approx(2.0, rel=0.02)
