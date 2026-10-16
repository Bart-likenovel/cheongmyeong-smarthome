"""입지 지도의 철도 표기·운행 상태 구분 회귀 검사. 사이트 루트에서 실행."""
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

SVG = Path(__file__).resolve().parents[1] / 'assets/img/svg/location-map.svg'
NS = {'s': 'http://www.w3.org/2000/svg'}


class RailwayMapTest(unittest.TestCase):
    def test_labels_and_key_lines_contrast_with_background(self):
        root = ET.parse(SVG).getroot()
        style = root.find('s:style', NS).text
        background = root.find('s:rect', NS).attrib['fill']

        def luminance(color):
            channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
            return sum(w * (v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4)
                       for v, w in zip(channels, [.2126, .7152, .0722]))

        def contrast(color):
            a, b = sorted([luminance(color), luminance(background)])
            return (b + .05) / (a + .05)

        for selector in ['.label-name', '.label-detail', '.rail .label-name',
                         '.rail .label-detail', '.planned-name', '.planned-sub',
                         '.legend', '.site-name', '.site-sub', '.cap', '.ringlbl']:
            rule = re.search(re.escape(selector) + r'\{([^}]+)\}', style)[1]
            color = re.search(r'fill:(#[0-9A-Fa-f]+)', rule)[1]
            self.assertGreaterEqual(contrast(color), 7, selector)
        for selector in ['.label-leader', '.rail-existing', '.rail-planned']:
            rule = re.search(re.escape(selector) + r'\{([^}]+)\}', style)[1]
            color = re.search(r'stroke:(#[0-9A-Fa-f]+)', rule)[1]
            self.assertGreaterEqual(contrast(color), 3, selector)

    def test_sinseong_distance_uses_owner_guidance(self):
        root = ET.parse(SVG).getroot()
        labels = [el.text or '' for el in root.findall('.//s:text', NS)]
        self.assertIn('용인신성초 · 0.5km(사업주 안내)', labels)
        self.assertFalse(any('용인신성초' in label and '0.7km' in label for label in labels))

    def test_stations_and_planned_route_are_visible_and_distinct(self):
        root = ET.parse(SVG).getroot()
        text = ''.join(root.itertext())
        for label in ['청명역', '상갈역', '수인·분당선', '인덕원–동탄', '개통 예정', '개략']:
            self.assertIn(label, text)
        style = root.find('s:style', NS).text
        colors = []
        for cls in ['rail-existing', 'rail-planned']:
            rule = re.search(r'\.' + cls + r'\{([^}]+)\}', style)
            self.assertIsNotNone(rule, cls)
            colors.append(re.search(r'stroke:(#[0-9A-Fa-f]+)', rule[1])[1])
        self.assertNotEqual(*colors)
        self.assertRegex(style, r'\.rail-planned\{[^}]*stroke-dasharray:')
        for cls in ['rail-existing', 'rail-planned']:
            self.assertTrue(root.findall(f'.//s:path[@class="{cls}"]', NS), cls)


if __name__ == '__main__':
    unittest.main()
