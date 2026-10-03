"""アームと倒立振子の概念図。描画座標は図の配置で、実機寸法ではない。"""

from pathlib import Path
import xml.etree.ElementTree as ET


NAMESPACE = "http://www.w3.org/2000/svg"
ET.register_namespace("", NAMESPACE)
OUTPUT = Path(__file__).resolve().parents[1] / "docs/_images"


def element(parent, tag, text=None, **attributes):
    node = ET.SubElement(parent, f"{{{NAMESPACE}}}{tag}", {
        key.replace("_", "-"): str(value) for key, value in attributes.items()
    })
    node.text = text
    return node


def canvas(title, description):
    svg = ET.Element(f"{{{NAMESPACE}}}svg", {
        "viewBox": "0 0 560 350", "role": "img", "aria-labelledby": "title description",
    })
    element(svg, "title", title, id="title")
    element(svg, "desc", description, id="description")
    element(svg, "rect", x=0, y=0, width=560, height=350, fill="white")
    defs = element(svg, "defs")
    marker = element(defs, "marker", id="arrow", viewBox="0 0 10 10", refX=9, refY=5, markerWidth=6, markerHeight=6, orient="auto")
    element(marker, "path", d="M 0 0 L 10 5 L 0 10 z", fill="#334155")
    return svg


def line(svg, x1, y1, x2, y2, **style):
    attributes = {"stroke": "#334155", "stroke_width": 2}
    attributes.update(style)
    return element(svg, "line", x1=x1, y1=y1, x2=x2, y2=y2, **attributes)


def label(svg, x, y, text):
    return element(svg, "text", text, x=x, y=y, fill="#0f172a", font_family="sans-serif", font_size=18)


def save(svg, name):
    OUTPUT.mkdir(parents=True, exist_ok=True)
    ET.indent(svg)
    destination = OUTPUT / name
    ET.ElementTree(svg).write(destination, encoding="utf-8", xml_declaration=True)
    print(destination)


def arm():
    svg = canvas("2軸平面アームの座標", "原点から第1リンク、第2リンクの順に先端へつながる。第1関節角はx軸から、第2関節角は第1リンクの延長から測る。")
    line(svg, 70, 260, 450, 260, marker_end="url(#arrow)")
    line(svg, 70, 260, 70, 40, marker_end="url(#arrow)")
    # 関節は (70,260), (230,200), (350,70)。リンク長の比は実機を表さない。
    element(svg, "path", d="M 70 260 L 230 200 L 350 70", fill="none", stroke="#2563eb", stroke_width=8)
    line(svg, 230, 200, 350, 155, stroke_dasharray="6 5")
    for x, y in [(70, 260), (230, 200), (350, 70)]:
        element(svg, "circle", cx=x, cy=y, r=7, fill="#0f172a")
    element(svg, "path", d="M 125 260 A 55 55 0 0 0 121.5 240.7", fill="none", stroke="#c2410c", stroke_width=2)
    element(svg, "path", d="M 281.5 180.7 A 55 55 0 0 0 267.3 159.6", fill="none", stroke="#c2410c", stroke_width=2)
    for x, y, text in [(35, 285, "原点"), (458, 265, "x"), (65, 30, "y"), (132, 253, "θ₁"), (284, 157, "θ₂"), (130, 211, "長さ l₁"), (310, 140, "長さ l₂"), (363, 72, "先端 (x, y)"), (60, 323, "θ₂ は第1リンクに対する相対角")]:
        label(svg, x, y, text)
    save(svg, "planar-arm.svg")


def cart_pole():
    svg = canvas("台車上の倒立振子", "台車位置pの正方向は右。振子角φは鉛直上向きから、先端が右へ傾く向きを正とする。入力Fは台車への水平力。")
    line(svg, 45, 295, 505, 295, marker_end="url(#arrow)")
    element(svg, "rect", x=150, y=235, width=160, height=45, rx=6, fill="#eff6ff", stroke="#2563eb", stroke_width=2)
    for x in [180, 280]:
        element(svg, "circle", cx=x, cy=285, r=10, fill="#334155")
    line(svg, 230, 235, 230, 45, stroke_dasharray="6 5")
    element(svg, "path", d="M 230 235 L 300 70", stroke="#2563eb", stroke_width=7)
    element(svg, "circle", cx=300, cy=70, r=15, fill="#2563eb")
    element(svg, "circle", cx=230, cy=235, r=6, fill="#0f172a")
    element(svg, "path", d="M 230 180 A 55 55 0 0 1 251.5 184.4", fill="none", stroke="#c2410c", stroke_width=2)
    line(svg, 320, 257, 440, 257, marker_end="url(#arrow)")
    for x, y, text in [(170, 36, "鉛直上向き：φ = 0"), (270, 187, "φ"), (288, 151, "長さ l"), (324, 76, "先端質量 m"), (190, 264, "台車 M"), (350, 245, "入力 F"), (128, 330, "台車位置 p の正方向 →")]:
        label(svg, x, y, text)
    save(svg, "cart-pole.svg")


if __name__ == "__main__":
    arm()
    cart_pole()
