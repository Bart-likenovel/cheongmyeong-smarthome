"""입지 지도 SVG 생성기.
좌표: 네이버지도 검색 결과(2026-10-11 조회). 청명초·삼성전자 수원사업장은 OpenStreetMap(2026-10-12 조회). 방향은 실제 방위, 거리는 단지 중심 직선거리.
반경은 가독성을 위해 제곱근 비율로 압축하고, 링에 실제 거리(500m·1km·3km)를 표기한다.
사용: python3 -I tools/build-location-map.py
"""
import math, os, json
from pathlib import Path

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "img", "svg", "location-map.svg")
CENTER = (37.2576975, 127.0894997)  # 하갈동 343-1
POIS = [  # 이름, 보조 설명, 위도, 경도, 라벨 위치(left/right/up)[, 표기 거리 km: 사업주 안내값으로 반경·숫자를 덮어쓸 때]
    ("청명산", "숲·산책로", 37.2585947, 127.0836475, "left"),
    ("청명초등학교", "수원 영통구", 37.2656313, 127.0852092, "left", 0.6),  # 사용자 지시(2026-10-13). OSM 좌표 직선거리는 약 1.0km
    ("삼성전자 수원사업장", "수원 영통구", 37.2572873, 127.0520942, "up"),
    ("신성초등학교", "용인신성초", 37.2553636, 127.0816460, "left", 0.5),  # 사용자 지시(2026-10-16): 사업주 안내 거리
    ("기흥중학교", "하갈동", 37.2588263, 127.0966821, "right"),
    ("청명호수마을", "생활권", 37.2541492, 127.0925468, "right"),
    ("기흥호수공원", "호수 산책", 37.2390828, 127.0998597, "right"),
    ("삼성전자 기흥캠퍼스", "농서동", 37.2295545, 127.0801901, "left"),
]
# 철도 좌표·개략 선형·출처 원본. 사이트 설명은 site-data.js에서 관리한다.
RAIL = json.loads((Path(__file__).with_name('rail-map-data.json')).read_text())
FAR = ("용인 반도체 국가산단", "처인구 이동·남사읍", 37.1450, 127.2100)  # 방향 표시용 개략 좌표(거리 미표기)
W, H, CX, CY = 800, 720, 400, 340
K = 168  # r = K * sqrt(km)

def offset_km(lat, lon):
    dx = (lon - CENTER[1]) * math.cos(math.radians(CENTER[0])) * 111.32
    dy = (lat - CENTER[0]) * 110.57
    return dx, dy

def place(lat, lon, dist=None):
    dx, dy = offset_km(lat, lon)
    d = dist or math.hypot(dx, dy)  # 방향은 좌표, 거리는 지정값 우선
    r = K * math.sqrt(d)
    h = math.hypot(dx, dy)
    return CX + dx / h * r, CY - dy / h * r, d

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
# 예정 철도: 공식 노선도의 흥덕–영통–서천 방향을 단순화한 개략 선형.
# 좌표는 위치 관계 표현용이며 측량·설계 선형이 아니다. 단지 경유를 의미하지 않는다.
route = [place(*p)[:2] for p in RAIL['planned']['points']]
parts.append('<path d="' + ' '.join(('M' if i == 0 else 'L') + f'{x:.1f} {y:.1f}' for i, (x, y) in enumerate(route)) + '" class="rail-planned"/>')
parts.append('<text x="32" y="66" class="planned-name">인덕원–동탄 복선전철</text>')
parts.append('<text x="32" y="86" class="planned-sub">개통 예정 · 흥덕–영통 구간 개략</text>')
parts.append('<text x="32" y="106" class="planned-sub">↑ 인덕원 방면 / ↓ 동탄 방면</text>')
# 지점
for name, sub, lat, lon, side, *dist in POIS:
    x, y, d = place(lat, lon, *dist)
    anchor, tx = ("end", x - 14) if side == "left" else ("start", x + 14)
    ty = y
    if side == "up":  # 왼쪽 가장자리 지점: 점 위로 라벨을 올려 다른 라벨과 겹치지 않게 한다
        anchor, tx, ty = "start", max(32, x - 50), y - 42
    parts.append(f'<line x1="{CX}" y1="{CY}" x2="{x:.1f}" y2="{y:.1f}" class="spoke"/>')
    parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" class="poi"/><circle cx="{x:.1f}" cy="{y:.1f}" r="12" class="poi-halo"/>')
    parts.append(f'<text x="{tx:.1f}" y="{ty - 2:.1f}" text-anchor="{anchor}" class="name">{name}</text>')
    distance_label = f"{sub} · {km(d)}(사업주 안내)" if dist else f"{sub} · 직선 {km(d)}"
    parts.append(f'<text x="{tx:.1f}" y="{ty + 17:.1f}" text-anchor="{anchor}" class="dist">{distance_label}</text>')
# 운행 중인 역: 기존 시설과 다른 노란색, 실제 좌표에서 계산한 직선거리.
for station in RAIL['stations']:
    x, y, d = place(*station['coords'])
    tx, ty = station['label']
    parts.append(f'<path d="M{x:.1f} {y:.1f} L{tx} {ty + 8}" class="rail-existing"/>')
    parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" class="rail-station"/>')
    parts.append(f'<text x="{tx}" y="{ty}" class="rail-name">{station["name"]}</text>')
    parts.append(f'<text x="{tx}" y="{ty + 20}" class="rail-sub">수인·분당선 · 직선 {km(d)}</text>')
# 범례: 색상과 선 종류로 운행/예정을 함께 구분한다.
parts.append('<path d="M480 55 H512" class="rail-existing"/><text x="522" y="60" class="rail-sub">운행 중인 역</text>')
parts.append('<path d="M480 80 H512" class="rail-planned"/><text x="522" y="85" class="planned-sub">예정 노선(개략)</text>')
# 원거리: 국가산단 방향 화살표
dx, dy = offset_km(FAR[2], FAR[3]); d = math.hypot(dx, dy)
ux, uy = dx / d, -dy / d
ex, ey = CX + ux * 380, CY + uy * 380
parts.append(f'<line x1="{CX + ux * 338:.1f}" y1="{CY + uy * 338:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" class="far" marker-end="url(#arrow)"/>')
parts.append(f'<text x="{W - 32}" y="{H - 78}" text-anchor="end" class="name">{FAR[0]}</text>')
parts.append(f'<text x="{W - 32}" y="{H - 58}" text-anchor="end" class="dist">{FAR[1]} 방향</text>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
  <title id="t">청명스마트AI홈 입지 지도</title>
  <desc id="d">하갈동 343-1 단지를 중심으로 주요 시설의 실제 방향과 직선거리를 나타낸 지도. 반경은 압축 표기. 노란색은 청명역·상갈역(수인·분당선), 주황 점선은 인덕원–동탄 개통 예정 노선의 개략 위치.</desc>
  <style>
    text{{font-family:'IBM Plex Sans KR','Apple SD Gothic Neo','Malgun Gothic',sans-serif}}
    .contour{{fill:none;stroke:#7DB043;stroke-width:1.2}}
    .ring{{fill:none;stroke:#DCEAF2;stroke-opacity:.22;stroke-width:1;stroke-dasharray:2 6}}
    .ringlbl{{font-size:12px;fill:#DCEAF2;fill-opacity:.55;letter-spacing:.04em}}
    .axis{{stroke:#DCEAF2;stroke-opacity:.07;stroke-width:1}}
    .spoke{{stroke:#C9D9B0;stroke-opacity:.35;stroke-width:1}}
    .poi{{fill:#DCEAF2}}
    .poi-halo{{fill:none;stroke:#DCEAF2;stroke-opacity:.3}}
    .name{{font-size:17px;font-weight:600;fill:#FBFCFC;paint-order:stroke;stroke:#142824;stroke-width:3}}
    .dist{{font-size:12.5px;fill:#B9CBC6;paint-order:stroke;stroke:#142824;stroke-width:3}}
    .far{{stroke:#7DB043;stroke-width:1.6;stroke-dasharray:6 6}}
    .rail-existing{{fill:none;stroke:#FFD35A;stroke-width:2.5}}
    .rail-planned{{fill:none;stroke:#FF9F70;stroke-width:4;stroke-dasharray:10 7;stroke-linecap:round}}
    .rail-station{{fill:#142824;stroke:#FFD35A;stroke-width:4}}
    .rail-name{{font-size:18px;font-weight:700;fill:#FFD35A;paint-order:stroke;stroke:#142824;stroke-width:4}}
    .rail-sub{{font-size:13px;fill:#FFD35A;paint-order:stroke;stroke:#142824;stroke-width:3}}
    .planned-name{{font-size:18px;font-weight:700;fill:#FF9F70}}
    .planned-sub{{font-size:13px;fill:#FFBC9B;paint-order:stroke;stroke:#142824;stroke-width:3}}
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
  <text x="{CX}" y="{CY - 2}" text-anchor="middle" class="site-name">청명스마트AI홈</text>
  <text x="{CX}" y="{CY + 18}" text-anchor="middle" class="site-sub">하갈동 343-1 일원</text>
  <g transform="translate({W - 56} 64)">
    <path d="M0 -20 L7 6 L0 1 L-7 6 Z" fill="#DCEAF2"/>
    <text x="-4" y="22" class="n">N</text>
  </g>
  <text x="32" y="{H - 36}" class="cap">거리: 청명초·신성초는 사업주 안내 / 그 외 단지 중심 직선거리 · 반경 축약</text>
  <text x="32" y="{H - 17}" class="cap">예정 노선: 지자체 공개자료 기반 개략도 · 실제 선형·역 위치 및 일정은 변경될 수 있습니다.</text>
</svg>
'''
open(OUT, "w", encoding="utf-8").write(svg)
print("wrote", OUT)
