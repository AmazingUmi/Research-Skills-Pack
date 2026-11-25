from pathlib import Path
import subprocess
import sys
import zipfile
from xml.etree import ElementTree as ET

import pytest
from PIL import Image

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_proposal_docx.py"


def test_word_embeds_source_artifacts_and_preserves_formatting(tmp_path):
    pytest.importorskip("latex2mathml")
    Image.new("RGB", (60, 20), "blue").save(tmp_path / "measurement.png")
    source = tmp_path / "proposal.md"
    source.write_text(r"""# 计划

**甲**与**乙**，含公式 $x_1$。

![实测](measurement.png)

$$
\frac{a}{b}
$$

| 描述 | 数值 |
| --- | --- |
| 条件概率 P(A\|B) | 0.5 |
""", encoding="utf-8")
    subprocess.run([sys.executable, str(SCRIPT), str(source)], cwd=tmp_path, check=True)
    with zipfile.ZipFile(source.with_suffix(".docx")) as package:
        assert any(path.startswith("word/media/") for path in package.namelist())
        root = ET.fromstring(package.read("word/document.xml"))
    ns = {"m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
          "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    assert len(root.findall(".//m:oMath", ns)) == 2
    assert root.find(".//m:f", ns) is not None
    assert root.find(".//m:sSub", ns) is not None
    runs = {r.findtext("w:t", namespaces=ns): r.find("w:rPr/w:b", ns) is not None
            for r in root.findall(".//w:r", ns)}
    assert runs["甲"] and runs["乙"] and not runs["与"]
    assert "条件概率 P(A|B)" in runs
