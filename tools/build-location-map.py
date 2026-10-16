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
W, H, CX, CY = 1000, 930, 500, 440
K = 190  # r = K * sqrt(km)

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

# 라벨 위치만 조정한다. 시설·거리·방위와 철도 개략 좌표는 유지한다.
LABELS = {
    "청명산": (420, 350, "end"),
    "청명초등학교": (475, 235, "start"),
    "삼성전자 수원사업장": (65, 500, "start"),
    "신성초등학교": (245, 600, "start"),
    "기흥중학교": (705, 455, "start"),
    "청명호수마을": (660, 590, "start"),
    "기흥호수공원": (700, 680, "start"),
    "삼성전자 기흥캠퍼스": (300, 815, "start"),
    "청명역": (85, 285, "start"),
    "상갈역": (770, 320, "start"),
}


def label(name, detail, x, y, rail=False):
    tx, ty, anchor = LABELS[name]
    dock_y = ty + 36 if y > ty + 36 else ty - 18
    cls = "rail" if rail else "facility"
    return (
        f'<path d="M{x:.1f} {y:.1f} V{dock_y} H{tx}" class="label-leader {cls}"/>'
        f'<g class="map-label {cls}">'
        f'<text x="{tx}" y="{ty}" text-anchor="{anchor}" class="label-name">{name}</text>'
        f'<text x="{tx}" y="{ty + 24}" text-anchor="{anchor}" class="label-detail">{detail}</text></g>'
    )


background, marks, labels = [], [], []
mx, my, _ = place(*POIS[0][2:4])
for i, r in enumerate([112, 88, 66, 44, 24]):
    background.append(f'<path d="{blob(mx - 30, my + 12, r, i * .7)}" class="contour"/>')
for dist, text in [(0.5, "500m"), (1, "1km"), (3, "3km")]:
    r = K * math.sqrt(dist)
    background.append(f'<circle cx="{CX}" cy="{CY}" r="{r:.1f}" class="ring"/>')
    background.append(f'<text x="{CX + r * .71 + 8:.1f}" y="{CY - r * .71:.1f}" class="ringlbl">{text}</text>')
background.append(f'<path d="M{CX} 165 V835 M45 {CY} H955" class="axis"/>')
route = [place(*point)[:2] for point in RAIL['planned']['points']]
background.append('<path d="' + ' '.join(('M' if i == 0 else 'L') + f'{x:.1f} {y:.1f}' for i, (x, y) in enumerate(route)) + '" class="rail-planned"/>')
for name, sub, lat, lon, side, *dist in POIS:
    x, y, d = place(lat, lon, *dist)
    background.append(f'<line x1="{CX}" y1="{CY}" x2="{x:.1f}" y2="{y:.1f}" class="spoke"/>')
    marks.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" class="poi-halo"/><circle cx="{x:.1f}" cy="{y:.1f}" r="5" class="poi"/>')
    detail = f"{sub} · {km(d)}(사업주 안내)" if dist else f"{sub} · 직선 {km(d)}"
    labels.append(label(name, detail, x, y))
for station in RAIL['stations']:
    x, y, d = place(*station['coords'])
    marks.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" class="rail-station"/><circle cx="{x:.1f}" cy="{y:.1f}" r="3" class="rail-dot"/>')
    labels.append(label(station['name'], f"수인·분당선 · 직선 {km(d)}", x, y, True))
dx, dy = offset_km(FAR[2], FAR[3]); d = math.hypot(dx, dy)
ux, uy = dx / d, -dy / d
ex, ey = CX + ux * 410, CY + uy * 410
marks.append(f'<line x1="{CX + ux * 370:.1f}" y1="{CY + uy * 370:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" class="far" marker-end="url(#arrow)"/>')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
  <title id="t">청명스마트AI홈 입지 지도</title>
  <desc id="d">하갈동 343-1 단지를 중심으로 주요 시설의 실제 방향과 직선거리를 나타낸 지도. 반경은 압축 표기. 노란색은 청명역·상갈역(수인·분당선), 주황 점선은 인덕원–동탄 개통 예정 노선의 개략 위치.</desc>
  <style>
    text{{font-family:'IBM Plex Sans KR','Apple SD Gothic Neo','Malgun Gothic',sans-serif}}
    .contour{{fill:none;stroke:#8AA692;stroke-width:1;opacity:.22}}
    .ring{{fill:none;stroke:#CAD8D2;stroke-width:1;stroke-dasharray:2 7}}
    .ringlbl{{font-size:15px;fill:#62766B}}
    .axis{{stroke:#D6E0DB;stroke-width:1;opacity:.38}}
    .spoke{{stroke:#B9CAC1;stroke-width:1;opacity:.28}}
    .poi{{fill:#496A5C}}
    .poi-halo{{fill:#F4F8F5;stroke:#B9CAC1;stroke-width:1}}
    .label-leader{{fill:none;stroke:#A7BCB0;stroke-width:1}}
    .label-leader.rail{{stroke:#BEA46A}}
    .label-name{{font-size:22px;font-weight:600;fill:#284A3C;paint-order:stroke;stroke:#F4F8F5;stroke-width:7;stroke-linejoin:round}}
    .label-detail{{font-size:15.5px;fill:#62766B;paint-order:stroke;stroke:#F4F8F5;stroke-width:6;stroke-linejoin:round}}
    .rail .label-name{{fill:#9B701B}}
    .rail .label-detail{{fill:#85692E}}
    .rail-existing{{fill:none;stroke:#B99236;stroke-width:2}}
    .rail-planned{{fill:none;stroke:#CA9170;stroke-width:2.5;stroke-dasharray:7 7;stroke-linecap:round}}
    .rail-station{{fill:#FFFFFF;stroke:#B99236;stroke-width:2.5}}
    .rail-dot{{fill:#B99236}}
    .planned-name{{font-size:22px;font-weight:600;fill:#8A6049}}
    .planned-sub{{font-size:15px;fill:#756150}}
    .legend{{font-size:15px;fill:#62766B}}
    .far{{stroke:#7C9A74;stroke-width:1.5;stroke-dasharray:5 6}}
    .site-name{{font-family:'Gowun Batang','Noto Serif KR',serif;font-size:21px;fill:#244B3A;font-weight:700}}
    .site-sub{{font-size:14px;fill:#62766B}}
    .cap{{font-size:14px;fill:#62766B}}
  </style>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="#7C9A74"/></marker>
  </defs>
  <rect width="{W}" height="{H}" fill="#F4F8F5"/>
  <path d="M45 145 H955 M45 864 H955" stroke="#D5E0D9" fill="none"/>
  <text x="50" y="58" class="planned-name">인덕원–동탄 복선전철</text>
  <text x="50" y="84" class="planned-sub">개통 예정 · 흥덕–영통 구간 개략</text>
  <text x="50" y="109" class="planned-sub">↑ 인덕원 방면 / ↓ 동탄 방면</text>
  <path d="M690 61 H722" class="rail-existing"/><text x="735" y="66" class="legend">운행 중인 역</text>
  <path d="M690 92 H722" class="rail-planned"/><text x="735" y="97" class="legend">예정 노선(개략)</text>
  <g transform="translate(949 72)"><path d="M0 -19 L6 5 L0 1 L-6 5 Z" fill="#567667"/><text x="-5" y="27" font-size="14" fill="#62766B">N</text></g>
  {"".join(background)}
  {"".join(labels)}
  {"".join(marks)}
  <circle cx="{CX}" cy="{CY}" r="92" fill="#F4F8F5" stroke="#D4E0D7"/>
  <circle cx="{CX}" cy="{CY}" r="85" fill="#FFFFFF" stroke="#9BB59F" stroke-width="1.3"/>
  <text x="{CX}" y="{CY - 3}" text-anchor="middle" class="site-name">청명스마트AI홈</text>
  <text x="{CX}" y="{CY + 23}" text-anchor="middle" class="site-sub">하갈동 343-1 일원</text>
  <text x="950" y="815" text-anchor="end" class="label-name">{FAR[0]}</text>
  <text x="950" y="839" text-anchor="end" class="label-detail">{FAR[1]} 방향</text>
  <text x="45" y="890" class="cap">거리: 청명초·신성초는 사업주 안내 / 그 외 단지 중심 직선거리 · 반경 축약</text>
  <text x="45" y="914" class="cap">예정 노선: 지자체 공개자료 기반 개략도 · 실제 선형·역 위치 및 일정은 변경될 수 있습니다.</text>
</svg>
'''
Path(OUT).write_text(svg, encoding="utf-8")
print("wrote", OUT)
