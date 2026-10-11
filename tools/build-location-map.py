"""입지 지도 SVG 생성기.
좌표: 네이버지도 검색 결과(2026-10-11 조회). 방향은 실제 방위, 거리는 단지 중심 직선거리.
반경은 가독성을 위해 제곱근 비율로 압축하고, 링에 실제 거리(500m·1km·3km)를 표기한다.
사용: python3 -I tools/build-location-map.py
"""
import math, os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "img", "svg", "location-map.svg")
CENTER = (37.2576975, 127.0894997)  # 하갈동 343-1
POIS = [  # 이름, 보조 설명, 위도, 경도, 라벨 위치(left/right)
    ("청명산", "숲·산책로", 37.2585947, 127.0836475, "left"),
    ("신성초등학교", "용인신성초", 37.2553636, 127.0816460, "left"),
    ("기흥중학교", "하갈동", 37.2588263, 127.0966821, "right"),
    ("청명호수마을", "생활권", 37.2541492, 127.0925468, "right"),
    ("기흥호수공원", "호수 산책", 37.2390828, 127.0998597, "right"),
    ("삼성전자 기흥캠퍼스", "농서동", 37.2295545, 127.0801901, "left"),
]
FAR = ("용인 반도체 국가산단", "처인구 이동·남사읍", 37.1450, 127.2100)  # 방향 표시용 개략 좌표(거리 미표기)
W, H, CX, CY = 800, 720, 400, 340
K = 168  # r = K * sqrt(km)

def offset_km(lat, lon):
    dx = (lon - CENTER[1]) * math.cos(math.radians(CENTER[0])) * 111.32
    dy = (lat - CENTER[0]) * 110.57
    return dx, dy

def place(lat, lon):
    dx, dy = offset_km(lat, lon)
    d = math.hypot(dx, dy)
    r = K * math.sqrt(d)
    return CX + dx / d * r, CY - dy / d * r, d

def km(d):
    return f"{d:.1f}km"

def blob(cx, cy, r, seed, n=9):
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = r * (1 + 0.18 * math.sin(3 * a + seed) + 0.08 * math.cos(5 * a + seed * 2))
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(n):
        p0, p1 = pts[i], pts[(i + 1) % n]
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        d += f" Q{p0[0]:.1f} {p0[1]:.1f} {mx:.1f} {my:.1f}"
    return d + " Z"

parts = []
# 청명산 등고선
mx, my, _ = place(*POIS[0][2:4])
for i, r in enumerate([112, 88, 66, 44, 24]):
    parts.append(f'<path d="{blob(mx - 30, my + 12, r, i * .7)}" class="contour" style="opacity:{.18 + i * .1:.2f}"/>')
# 거리 링
for dist, label in [(0.5, "500m"), (1, "1km"), (3, "3km")]:
    r = K * math.sqrt(dist)
    parts.append(f'<circle cx="{CX}" cy="{CY}" r="{r:.1f}" class="ring"/>')
    parts.append(f'<text x="{CX + r * .71 + 6:.1f}" y="{CY - r * .71:.1f}" class="ringlbl">{label}</text>')
# 방위선
parts.append(f'<path d="M{CX} 40 V{H - 40} M60 {CY} H{W - 60}" class="axis"/>')
# 지점
for name, sub, lat, lon, side in POIS:
    x, y, d = place(lat, lon)
    anchor, tx = ("end", x - 14) if side == "left" else ("start", x + 14)
    parts.append(f'<line x1="{CX}" y1="{CY}" x2="{x:.1f}" y2="{y:.1f}" class="spoke"/>')
    parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" class="poi"/><circle cx="{x:.1f}" cy="{y:.1f}" r="12" class="poi-halo"/>')
    parts.append(f'<text x="{tx:.1f}" y="{y - 2:.1f}" text-anchor="{anchor}" class="name">{name}</text>')
    parts.append(f'<text x="{tx:.1f}" y="{y + 17:.1f}" text-anchor="{anchor}" class="dist">{sub} · 직선 {km(d)}</text>')
# 원거리: 국가산단 방향 화살표
dx, dy = offset_km(FAR[2], FAR[3]); d = math.hypot(dx, dy)
ux, uy = dx / d, -dy / d
ex, ey = CX + ux * 380, CY + uy * 380
parts.append(f'<line x1="{CX + ux * 338:.1f}" y1="{CY + uy * 338:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" class="far" marker-end="url(#arrow)"/>')
parts.append(f'<text x="{W - 32}" y="{H - 78}" text-anchor="end" class="name">{FAR[0]}</text>')
parts.append(f'<text x="{W - 32}" y="{H - 58}" text-anchor="end" class="dist">{FAR[1]} 방향</text>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
  <title id="t">청명스마트홈 입지 지도</title>
  <desc id="d">하갈동 343-1 단지를 중심으로 주요 시설의 실제 방향과 직선거리를 나타낸 지도. 반경은 압축 표기.</desc>
  <style>
    text{{font-family:'IBM Plex Sans KR','Apple SD Gothic Neo','Malgun Gothic',sans-serif}}
    .contour{{fill:none;stroke:#7DB043;stroke-width:1.2}}
    .ring{{fill:none;stroke:#DCEAF2;stroke-opacity:.22;stroke-width:1;stroke-dasharray:2 6}}
    .ringlbl{{font-size:12px;fill:#DCEAF2;fill-opacity:.55;letter-spacing:.04em}}
    .axis{{stroke:#DCEAF2;stroke-opacity:.07;stroke-width:1}}
    .spoke{{stroke:#C9D9B0;stroke-opacity:.35;stroke-width:1}}
    .poi{{fill:#DCEAF2}}
    .poi-halo{{fill:none;stroke:#DCEAF2;stroke-opacity:.3}}
    .name{{font-size:17px;font-weight:600;fill:#FBFCFC}}
    .dist{{font-size:12.5px;fill:#B9CBC6}}
    .far{{stroke:#7DB043;stroke-width:1.6;stroke-dasharray:6 6}}
    .site-name{{font-family:'Gowun Batang','Noto Serif KR',serif;font-size:17px;letter-spacing:-.02em;fill:#142824;font-weight:700}}
    .site-sub{{font-size:11.5px;fill:#2F4F48}}
    .cap{{font-size:12px;fill:#8FA7A1}}
    .n{{font-size:12px;fill:#DCEAF2;fill-opacity:.7}}
  </style>
  <defs>
    <radialGradient id="bg" cx="50%" cy="47%" r="70%">
      <stop offset="0" stop-color="#24443D"/><stop offset="1" stop-color="#101F1C"/>
    </radialGradient>
    <radialGradient id="glow"><stop offset="0" stop-color="#7DB043" stop-opacity=".55"/><stop offset="1" stop-color="#7DB043" stop-opacity="0"/></radialGradient>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M0 0 L10 5 L0 10 Z" fill="#7DB043"/>
    </marker>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  {"".join(parts)}
  <circle cx="{CX}" cy="{CY}" r="90" fill="url(#glow)"/>
  <circle cx="{CX}" cy="{CY}" r="62" fill="#FBFCFC"/>
  <circle cx="{CX}" cy="{CY}" r="69" fill="none" stroke="#7DB043" stroke-width="1.5"/>
  <text x="{CX}" y="{CY - 2}" text-anchor="middle" class="site-name">청명스마트홈</text>
  <text x="{CX}" y="{CY + 18}" text-anchor="middle" class="site-sub">하갈동 343-1 일원</text>
  <g transform="translate({W - 56} 64)">
    <path d="M0 -20 L7 6 L0 1 L-7 6 Z" fill="#DCEAF2"/>
    <text x="-4" y="22" class="n">N</text>
  </g>
  <text x="32" y="{H - 24}" class="cap">방향은 실제 방위, 거리는 단지 중심 직선거리 · 반경은 축약 표기 · 좌표 출처 네이버지도</text>
</svg>
'''
open(OUT, "w", encoding="utf-8").write(svg)
print("wrote", OUT)
