#!/usr/bin/env python3
import argparse
import json
import subprocess
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

W = 1080
H = 1680
DEFAULT_FONT = "'PingFang SC', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', sans-serif"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def q(s: str) -> str:
    return '"' + s.replace('"', '&quot;') + '"'


def wrap(text: str, width: int):
    return textwrap.wrap(text, width=width, break_long_words=False, break_on_hyphens=False)


def text_block(lines, x, y, size, color, font, weight='500', gap=1.35):
    out = []
    for i, line in enumerate(lines):
        out.append(
            f"<text x='{x}' y='{y + i * size * gap}' font-family={q(font)} font-size='{size}' fill='{color}' font-weight='{weight}'>{escape(line)}</text>"
        )
    return '\n'.join(out)


def rect(x, y, w, h, rx, fill, stroke='none', sw=0, opacity=1):
    return f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{rx}' fill='{fill}' stroke='{stroke}' stroke-width='{sw}' opacity='{opacity}'/>"


def card(parts, x, y, w, h, accent, accent2, font, item):
    parts.append(rect(x, y, w, h, 32, '#FFFFFF', '#E7EDF3', 2))
    parts.append(rect(x + 26, y + 24, 74, 40, 20, '#FFF1E7'))
    parts.append(text_block([item['num']], x + 46, y + 51, 24, accent, font, '800'))
    parts.append(text_block(wrap(item['title'], 16), x + 28, y + 112, 38, accent2, font, '800', 1.12))
    parts.append(text_block(['怎么用'], x + 28, y + 210, 24, accent, font, '700'))
    parts.append(text_block(wrap(item['use'], 22), x + 28, y + 250, 28, '#4C5A6A', font, '500', 1.4))
    parts.append(text_block(['为什么火'], x + 28, y + 358, 24, accent, font, '700'))
    parts.append(text_block(wrap(item['why'], 22), x + 28, y + 398, 28, '#4C5A6A', font, '500', 1.4))


def render_cover(slide, font):
    accent, accent2 = slide['accent'], slide['accent2']
    parts = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' viewBox='0 0 {W} {H}'>"]
    parts.append('<defs>')
    parts.append(f"<linearGradient id='bg' x1='0' y1='0' x2='1' y2='1'><stop offset='0%' stop-color='{slide['bg1']}'/><stop offset='100%' stop-color='{slide['bg2']}'/></linearGradient>")
    parts.append('</defs>')
    parts.append(rect(0, 0, W, H, 0, 'url(#bg)'))
    parts.append(f"<circle cx='918' cy='120' r='175' fill='{accent}' opacity='0.08'/>")
    parts.append(f"<circle cx='90' cy='1550' r='150' fill='{accent}' opacity='0.07'/>")
    parts.append(rect(64, 72, 952, 1536, 42, '#FFFFFF', opacity=0.95))
    parts.append(rect(96, 128, 170, 48, 24, '#F8E5CF'))
    parts.append(text_block([slide['badge']], 126, 160, 26, accent, font, '700'))
    parts.append(text_block(slide['title_lines'], 96, 260, 70, accent2, font, '800', 1.06))
    parts.append(text_block(wrap(slide['subtitle'], 26), 96, 500, 30, '#596679', font, '500', 1.45))
    chip_specs = [(96, 690, 220), (340, 690, 252), (616, 690, 220), (96, 800, 220), (340, 800, 220), (584, 800, 252)]
    for chip, (x, y, w) in zip(slide['chips'], chip_specs):
        parts.append(rect(x, y, w, 88, 24, '#FFFFFF', '#E6EDF2', 2))
        parts.append(text_block([chip], x + 26, y + 54, 28, accent2, font, '700'))
    parts.append(rect(96, 964, 888, 284, 28, '#F7F8FA'))
    parts.append(text_block(['这次整理的判断标准'], 126, 1022, 38, accent2, font, '800'))
    points = slide.get('points', [
        '最近社区案例、教程、云厂商指南里反复出现的用法',
        '必须是执行型场景，不是单纯“陪聊”或“问答”',
        '优先挑能直接节省时间、能复用、能持续跑的方向'
    ])
    cy = 1094
    for p in points:
        parts.append(f"<circle cx='140' cy='{cy - 8}' r='6' fill='{accent}'/>")
        parts.append(text_block(wrap(p, 31), 162, cy, 28, '#536071', font, '500', 1.42))
        cy += 92
    parts.append(rect(96, 1324, 888, 116, 30, '#FFF7EE', accent, 2))
    parts.append(text_block(wrap(slide['footer'], 38), 124, 1390, 28, accent2, font, '700', 1.34))
    parts.append('</svg>')
    return '\n'.join(parts)


def render_pair(slide, font):
    accent, accent2 = slide['accent'], slide['accent2']
    parts = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' viewBox='0 0 {W} {H}'>"]
    parts.append('<defs>')
    parts.append(f"<linearGradient id='bg' x1='0' y1='0' x2='1' y2='1'><stop offset='0%' stop-color='{slide['bg1']}'/><stop offset='100%' stop-color='{slide['bg2']}'/></linearGradient>")
    parts.append('</defs>')
    parts.append(rect(0, 0, W, H, 0, 'url(#bg)'))
    parts.append(f"<circle cx='918' cy='120' r='175' fill='{accent}' opacity='0.08'/>")
    parts.append(f"<circle cx='90' cy='1550' r='150' fill='{accent}' opacity='0.07'/>")
    parts.append(rect(64, 72, 952, 1536, 42, '#FFFFFF', opacity=0.95))
    parts.append(rect(96, 126, 184, 48, 24, '#F8E5CF'))
    parts.append(text_block([slide['header']], 126, 160, 26, accent, font, '700'))
    parts.append(text_block(wrap(slide['subheader'], 28), 96, 246, 34, accent2, font, '800', 1.35))
    card(parts, 96, 382, 888, 468, accent, accent2, font, slide['cards'][0])
    card(parts, 96, 892, 888, 468, accent, accent2, font, slide['cards'][1])
    parts.append(rect(96, 1402, 888, 84, 28, '#FFF7EE', accent, 2))
    parts.append(text_block(wrap(slide['footer'], 42), 122, 1454, 24, accent2, font, '700', 1.3))
    parts.append('</svg>')
    return '\n'.join(parts)


def render(slide, font):
    if slide['type'] == 'cover':
        return render_cover(slide, font)
    if slide['type'] == 'pair':
        return render_pair(slide, font)
    raise ValueError(f"Unsupported slide type: {slide['type']}")


def make_png(svg_path: Path, png_path: Path):
    subprocess.run([
        CHROME,
        '--headless=new',
        '--disable-gpu',
        '--hide-scrollbars',
        f'--window-size={W},{H}',
        f'--screenshot={png_path}',
        f'file://{svg_path}'
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--spec', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding='utf-8'))
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    font = spec.get('theme', {}).get('font', DEFAULT_FONT)

    for slide in spec['slides']:
        svg_path = out_dir / slide['filename']
        svg_path.write_text(render(slide, font), encoding='utf-8')
        make_png(svg_path, svg_path.with_suffix(svg_path.suffix + '.png'))

    print(f"generated {len(spec['slides'])} slides in {out_dir}")


if __name__ == '__main__':
    main()
