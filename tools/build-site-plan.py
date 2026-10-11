"""13필지 배치 개념도 SVG 생성기.
좌표는 참고자료/도면원본_codex_수정.png(1492×1054 px, 도로공사용도면 1/600)의 픽셀 좌표를 그대로 옮긴 것이다.
지번·소유자명은 넣지 않는다. 수정은 이 파일에서 하고 다시 실행한다.
사용: python3 -I tools/build-site-plan.py
"""
import math, os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "img", "svg", "site-plan.svg")
VB = (80, 160, 600, 760)  # x, y, w, h (도면 픽셀 좌표 기준 크롭)

# 단지 경계(도면 적색/흑색 경계선)
BOUNDARY = [(325, 282), (363, 283), (440, 257), (455, 270), (470, 300), (565, 330), (550, 363), (557, 440),
            (547, 460), (500, 560), (493, 593), (500, 600), (520, 707), (543, 740), (560, 803), (587, 840),
            (600, 892), (520, 857), (473, 817), (363, 740), (227, 677), (200, 660), (130, 590), (140, 517),
            (200, 440), (307, 303)]
# 북측 기존 도로(전면 도로) 중심선
FRONT_ROAD = [(80, 192), (165, 233), (245, 256), (330, 268), (440, 244), (500, 262), (630, 280), (700, 250),
              (750, 205), (790, 182)]
# 단지 내 도로 중심선: 진입부 → 꺾임점 → 남동 끝
INNER_ROAD = [(482, 262), (480, 300), (272, 594), (533, 756)]
# 구거(수로) 중심선
DITCH = [(80, 585), (190, 662), (330, 735), (420, 792), (520, 862), (610, 902)]
# 건물 13동 중심 좌표 (도면 해치 영역 중심)
HOUSES = [(383, 328), (307, 378), (262, 420), (217, 493), (178, 582),   # 진입로 서측 1~5
          (498, 393), (463, 437), (412, 507), (368, 562),               # 진입로 동측 6~9
          (295, 653), (458, 653), (415, 747), (523, 822)]               # 꺾인 도로 10~13
HOUSE_W, HOUSE_H, ROT = 62, 50, 35.3  # 도로 방향(-54.7°)에 맞춘 회전

def pts(seq):
    return " ".join(f"{x},{y}" for x, y in seq)

def path(seq):
    return "M" + " L".join(f"{x} {y}" for x, y in seq)

# 필지 구분선: 진입로/꺾인 도로 축에 수직인 선을 건물 사이 중간 지점에 긋고 경계로 자른다
def dividers():
    lines = []
    def axis_splits(a, b, idxs):
        ax, ay = b[0] - a[0], b[1] - a[1]
        L = math.hypot(ax, ay); ux, uy = ax / L, ay / L
        px, py = -uy, ux
        t = sorted(((HOUSES[i][0] - a[0]) * ux + (HOUSES[i][1] - a[1]) * uy) for i in idxs)
        for k in range(len(t) - 1):
            m = (t[k] + t[k + 1]) / 2
            cx, cy = a[0] + ux * m, a[1] + uy * m
            lines.append(((cx - px * 220, cy - py * 220), (cx + px * 220, cy + py * 220)))
    axis_splits(INNER_ROAD[1], INNER_ROAD[2], range(0, 5))
    axis_splits(INNER_ROAD[1], INNER_ROAD[2], range(5, 9))
    axis_splits(INNER_ROAD[2], INNER_ROAD[3], [9, 11])
    axis_splits(INNER_ROAD[2], INNER_ROAD[3], [10, 12])
    return lines

houses = []
for i, (x, y) in enumerate(HOUSES):
    d = 0.08 * i
    houses.append(
        f'<g transform="translate({x} {y})">'
        f'<rect class="house" x="{-HOUSE_W/2}" y="{-HOUSE_H/2}" width="{HOUSE_W}" height="{HOUSE_H}" '
        f'transform="rotate({ROT})" style="animation-delay:{d:.2f}s"/>'
        f'<text class="num" y="5" style="animation-delay:{d:.2f}s">{i+1}</text></g>')

div_lines = "\n    ".join(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}"/>' for a, b in dividers())

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VB[0]} {VB[1]} {VB[2]} {VB[3]}" role="img" aria-labelledby="t d">
  <title id="t">청명스마트홈 13필지 배치 개념도</title>
  <desc id="d">도로공사용 도면을 바탕으로 그린 배치 개념도. 북측 전면 도로에서 단지 진입로가 남서쪽으로 내려와 남동쪽으로 꺾이고, 진입로 양쪽과 꺾인 도로 주변에 주택 13동이 놓인다. 남서쪽 경계를 따라 구거가 흐른다.</desc>
  <style>
    .site{{fill:#FBFCFC;stroke:#1E3A34;stroke-width:2;stroke-dasharray:8 5}}
    .div line{{stroke:#A9C3CF;stroke-width:1.4;stroke-dasharray:5 4}}
    .house{{fill:#DCEAF2;stroke:#1E3A34;stroke-width:1.6;opacity:0;animation:in .45s ease forwards}}
    .num{{font:700 15px 'IBM Plex Sans KR',sans-serif;fill:#1E3A34;text-anchor:middle;opacity:0;animation:in .45s ease forwards}}
    .lbl{{font:500 14px 'IBM Plex Sans KR',sans-serif;fill:#1E3A34}}
    .sub{{font:400 12px 'IBM Plex Sans KR',sans-serif;fill:#4A6560}}
    @keyframes in{{to{{opacity:1}}}}
    @media (prefers-reduced-motion:reduce){{.house,.num{{animation:none;opacity:1}}}}
  </style>
  <rect x="{VB[0]}" y="{VB[1]}" width="{VB[2]}" height="{VB[3]}" fill="#F3F8FA"/>
  <defs><clipPath id="clip"><polygon points="{pts(BOUNDARY)}"/></clipPath></defs>
  <!-- 구거 -->
  <path d="{path(DITCH)}" fill="none" stroke="#C7DCC0" stroke-width="34" stroke-linecap="round"/>
  <path d="{path(DITCH)}" fill="none" stroke="#9CC27A" stroke-width="1.5" stroke-dasharray="3 5"/>
  <text x="285" y="772" class="sub" transform="rotate(25 285 772)">구거(수로)</text>
  <!-- 전면 도로 -->
  <path d="{path(FRONT_ROAD)}" fill="none" stroke="#C9D6DC" stroke-width="28" stroke-linejoin="round"/>
  <path d="{path(FRONT_ROAD)}" fill="none" stroke="#FBFCFC" stroke-width="1.5" stroke-dasharray="12 10"/>
  <text x="520" y="232" class="lbl">전면 도로 · 8m 개통 예정</text>
  <!-- 단지 -->
  <polygon class="site" points="{pts(BOUNDARY)}"/>
  <g class="div" clip-path="url(#clip)">
    {div_lines}
  </g>
  <path d="{path(INNER_ROAD)}" fill="none" stroke="#C9D6DC" stroke-width="34" stroke-linejoin="round" clip-path="url(#clip)"/>
  <path d="{path(INNER_ROAD[:2])}" fill="none" stroke="#C9D6DC" stroke-width="34"/>
  <text x="492" y="300" class="sub">단지 진입</text>
  {"".join(houses)}
  <text x="110" y="330" class="sub">인접 기허가지</text>
  <text x="575" y="520" class="sub">인접 기허가지</text>
  <!-- 방위 -->
  <g transform="translate(130 860)">
    <circle r="22" fill="none" stroke="#1E3A34" stroke-width="1.2"/>
    <path d="M0 -18 L6 4 L0 0 L-6 4 Z" fill="#1E3A34"/>
    <text x="-5" y="-27" class="sub">N</text>
  </g>
  <text x="200" y="905" class="sub">도로공사용 도면 기반 개념도 · 필지 경계와 건물 배치는 확정 설계와 다를 수 있습니다</text>
</svg>
'''
open(OUT, "w", encoding="utf-8").write(svg)
print("wrote", OUT)
