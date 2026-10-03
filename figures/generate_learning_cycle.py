"""学習手順図を生成する。Python標準ライブラリのみ。物理データは使わない。"""

from pathlib import Path
import xml.etree.ElementTree as ET


def generate() -> Path:
    namespace = "http://www.w3.org/2000/svg"
    ET.register_namespace("", namespace)

    def element(parent, tag, text=None, **attributes):
        node = ET.SubElement(parent, f"{{{namespace}}}{tag}", attributes)
        node.text = text
        return node

    svg = ET.Element(f"{{{namespace}}}svg", {
        "viewBox": "0 0 780 300", "role": "img",
        "aria-labelledby": "cycle-title cycle-description",
    })
    element(svg, "title", "実験と改良を繰り返す学習", id="cycle-title")
    element(svg, "desc", "問い、予想、工作・プログラミング、実験・計測、整理・考察、改良の順に進み、予想に戻ります。", id="cycle-description")
    element(svg, "rect", x="0", y="0", width="780", height="300", fill="white")
    defs = element(svg, "defs")
    marker = element(defs, "marker", id="arrow", viewBox="0 0 10 10", refX="9", refY="5", markerWidth="7", markerHeight="7", orient="auto-start-reverse")
    element(marker, "path", d="M 0 0 L 10 5 L 0 10 z", fill="#334155")
    for route in ["M 250 75 H 280", "M 500 75 H 530", "M 640 115 V 175", "M 530 215 H 500", "M 280 215 H 250", "M 140 175 V 145 H 390 V 115"]:
        element(svg, "path", d=route, fill="none", stroke="#334155", **{"stroke-width": "2", "marker-end": "url(#arrow)"})
    steps = [(30, 35, "問い"), (280, 35, "予想"), (530, 35, "工作・プログラミング"), (530, 175, "実験・計測"), (280, 175, "整理・考察"), (30, 175, "改良")]
    for x, y, label in steps:
        element(svg, "rect", x=str(x), y=str(y), width="220", height="80", rx="12", fill="#eff6ff", stroke="#2563eb")
        element(svg, "text", label, x=str(x + 110), y=str(y + 46), fill="#0f172a", **{"text-anchor": "middle", "font-size": "18", "font-family": "sans-serif"})
    output = Path(__file__).resolve().parents[1] / "docs/_images/learning-cycle.svg"
    output.parent.mkdir(parents=True, exist_ok=True)
    ET.indent(svg)
    ET.ElementTree(svg).write(output, encoding="utf-8", xml_declaration=True)
    return output


if __name__ == "__main__":
    print(generate())
