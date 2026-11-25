from pathlib import Path
import sys

from pptx import Presentation

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from audit_pptx_quality import audit_pptx


def test_master_placeholder_content_follows_presentation_order(tmp_path):
    deck = Presentation()
    first = deck.slides.add_slide(deck.slide_layouts[1])
    first.shapes.title.text = "一句话总结"
    first.placeholders[1].text = "内容" * 2500
    second = deck.slides.add_slide(deck.slide_layouts[1])
    second.shapes.title.text = "研究问题"
    deck.slides._sldIdLst.insert(0, deck.slides._sldIdLst[-1])
    path = tmp_path / "talk.pptx"
    deck.save(path)
    result = audit_pptx(path)
    findings = {(f["slide"], f["code"]) for f in result["findings"]}
    assert (2, "ai_template_phrase") in findings
    assert (2, "text_overload") in findings
    assert (1, "ai_template_phrase") not in findings
