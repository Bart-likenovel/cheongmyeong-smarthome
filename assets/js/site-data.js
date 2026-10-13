/* 청명스마트AI홈 사이트 공통 데이터 (SSOT)
 * 연락처·메뉴·사업개요·타입·입지·언론보도는 이 파일만 수정한다.
 * fact: 확인된 사실 / owner: 사업주(대표) 안내 / plan: 계획·검토 단계
 */
// 대표 지번(15필지 모두 사업주 소유, 필지별 지번은 상담 시 안내)
var ADDRESS = "경기도 용인시 기흥구 하갈동 343-1 일원";

window.SITE = {
  brand: { name: "청명스마트AI홈", en: "Cheongmyeong Smart AI Home", owner: "유만식" },
  contact: { tel: "010-5001-6182" },
  address: ADDRESS,
  mapQuery: "경기도 용인시 기흥구 하갈동 343-1",

  nav: [
    { label: "사업개요", href: "overview.html" },
    { label: "프리미엄", href: "premium.html" },
    { label: "입지환경", href: "location.html" },
    {
      label: "단지안내", href: "design.html",
      children: [
        { label: "단지조경", href: "design.html" },
        { label: "타입별 모듈주택", href: "unit.html" },
      ],
    },
    {
      label: "홍보센터", href: "news.html",
      children: [{ label: "언론보도", href: "news.html" }],
    },
  ],

  // 서브 비주얼: 서브 로고 + 영문 타이틀(h3) + 국문 카테고리(p)
  pages: {
    overview: { en: "overview", ko: "사업개요", img: "assets/img/ai/hero-01-village-v2.jpg" },
    premium: { en: "premium", ko: "프리미엄", img: "assets/img/ai/hero-03-interior-v2.jpg" },
    location: { en: "location", ko: "입지환경", img: "assets/img/ai/hero-05-trail.jpg" },
    design: { en: "landscape", ko: "단지안내", img: "assets/img/ai/landscape-v4.jpg" },
    unit: { en: "house types", ko: "단지안내", img: "assets/img/ai/hero-02-yard.jpg" },
    news: { en: "news", ko: "홍보센터", img: "assets/img/ai/hero-06-dusk.jpg" },
  },

  overview: [
    ["사업명", "청명스마트AI홈"],
    ["위치", ADDRESS + " (필지별 지번은 상담 시 안내)"],
    ["대지면적", "약 1,900평 (상세 면적 추후 안내)"],
    ["세대수", "15세대 (15필지)"],
    ["주택 유형", "모듈형 AI 스마트 단독주택 (A~E 5개 타입 검토 중)"],
    ["건축규모", "추후 안내"],
    ["연면적", "추후 안내"],
  ],

  // 타입별 모듈주택 공통: 평형은 설계 확정 후 안내
  typeSize: "평형 추후 안내",
  types: [
    {
      id: "a", name: "A타입", title: "모던 컴팩트",
      img: "assets/img/ai/type-a.jpg",
      spec: [["층수", "2층"], ["스타일", "모던"], ["설계", "모듈 설계"]],
      points: [
        "모듈 단위로 설계해 생활 변화에 따라 공간을 이동·확장할 수 있는 구조",
        "정면에서 현관이 보이지 않도록 배치해 사생활 보호",
        "넓은 포치로 작은 평형에서도 여유로운 외부 공간 확보",
      ],
    },
    {
      id: "b", name: "B타입", title: "오픈 거실 2층",
      img: "assets/img/ai/type-b.jpg",
      spec: [["구조", "경량목구조"], ["거실", "1.5층 오픈"], ["지붕", "아스팔트 싱글"],
             ["외부 마감", "스타코 / 파벽돌 / 징크 / 스마트우드 / 인조석"]],
      points: [
        "1층에 주요 생활 공간, 2층은 약 절반 규모로 구성",
        "거실 상부를 1.5층 높이로 열어 개방감 확보",
        "1층 전면 데크와 2층 발코니",
      ],
    },
    {
      id: "c", name: "C타입", title: "세미모던 패밀리",
      img: "assets/img/ai/type-c.jpg",
      spec: [["스타일", "세미모던"],
             ["외장", "세라믹 사이딩 / 알루미늄 루버"]],
      points: [
        "주요 공간을 남측에 배치해 조망과 일조 확보",
        "계단창으로 거실까지 빛이 들도록 계획",
        "도로보다 높은 대지를 활용한 마당과 하부 주차",
      ],
    },
    {
      id: "d", name: "D타입", title: "내추럴 목조",
      img: "assets/img/ai/type-d.jpg",
      spec: [["구조", "경량목구조"], ["층수", "2층"], ["외부 공간", "마당(잔디) / 텃밭(흙) / 휴식(파쇄석)"]],
      points: [
        "정면 통창과 상부 세로 창으로 풍경을 실내에 들임",
        "안방과 서재를 마주 보게 배치하고 가벽으로 영역 구분",
        "외부 바닥 재료를 용도별로 달리해 마당·텃밭·휴식 공간 분리",
      ],
    },
    {
      id: "e", name: "E타입", title: "클래식 적벽돌",
      img: "assets/img/ai/type-e.jpg",
      spec: [["외장", "적벽돌 (일부 들여쌓기)"], ["지붕", "비대칭 금속 지붕"], ["층수", "2층"]],
      points: [
        "적벽돌과 들여쌓기로 깔끔하면서도 클래식한 외관",
        "비대칭 지붕과 많은 창으로 보는 방향마다 다른 인상",
        "큰 고정창과 시스템 창으로 전 층에서 트인 조망",
      ],
    },
  ],

  // 입지 근거. kind: fact(보도·공식 확인) / owner(사업주 안내)
  location: [
    { title: "청명산 기슭", body: "청명산이 단지 서쪽 직선 약 0.5km에 있습니다. 숲과 계곡을 곁에 둔 조용한 주거지입니다.", kind: "fact", src: { label: "네이버지도 좌표 기준 직선거리", url: "https://map.naver.com/p/search/%EA%B2%BD%EA%B8%B0%EB%8F%84%20%EC%9A%A9%EC%9D%B8%EC%8B%9C%20%EA%B8%B0%ED%9D%A5%EA%B5%AC%20%ED%95%98%EA%B0%88%EB%8F%99%20343-1" } },
    { title: "8m 전면 진입 도시계획도로", body: "단지 앞 기존 도로를 8m로 넓히는 도시계획도로 공사가 2027년 7월 완공될 예정입니다.", kind: "owner" },
    { title: "초등학교 도보권", body: "용인신성초등학교가 단지에서 직선 약 0.7km 거리에 있습니다.", kind: "fact", src: { label: "네이버지도 좌표 기준 직선거리", url: "https://map.naver.com/p/search/%EA%B2%BD%EA%B8%B0%EB%8F%84%20%EC%9A%A9%EC%9D%B8%EC%8B%9C%20%EA%B8%B0%ED%9D%A5%EA%B5%AC%20%ED%95%98%EA%B0%88%EB%8F%99%20343-1" } },
    {
      title: "하갈동 중학교 신설", kind: "owner",
      body: "하갈동 기흥중학교가 단지에서 직선 약 0.6km 거리에 새로 들어서며, 2027년 2월 개교할 예정입니다.",
    },
    {
      title: "삼성전자 기흥·수원 직주근접", kind: "owner",
      body: "삼성전자 기흥캠퍼스(기흥구 농서동, 직선 약 3.2km)와 수원사업장(영통구, 직선 약 3.3km)까지 약 10~13분 거리의 생활권입니다.",
    },
    { title: "청명IC·수원신갈IC", kind: "owner", body: "용인-서울고속도로 청명IC와 맞닿아 있고, 경부고속도로 수원신갈IC에서 약 6분 거리입니다." },
    { title: "광역버스로 강남 35분", kind: "owner", body: "국도변 광역버스 노선으로 강남역까지 약 35분이면 닿아 강남 접근성이 뛰어납니다." },
    {
      title: "용인 반도체 국가산단", kind: "fact",
      body: "용인시 처인구 이동·남사읍 일대에 삼성전자 반도체 국가산업단지가 조성 중입니다.",
      src: { label: "한국일보 2025-03-14", url: "https://www.hankookilbo.com/News/Read/A2025031408370001371" },
    },
  ],

  news: [
    {
      press: "헤럴드경제", date: "2026-06-24",
      title: "“삼성전자가 단독주택도 만든다고?”…‘삼성 AI 모듈러 홈’ 3년 후 1만호 공급 목표",
      url: "https://biz.heraldcorp.com/article/10787219",
    },
    {
      press: "비즈니스포스트", date: "2026-06-24",
      title: "[현장] \"30평짜리 주택 만드는 비용 1억5천\", 삼성전자 'AI 모듈러 홈'으로 단독주택 개념 바꾼다",
      url: "https://www.businesspost.co.kr/BP?command=article_view&num=440747",
    },
    {
      press: "국제뉴스", date: "2026-10-09",
      title: "용인 기흥호수공원 '문화·체육 공간' 조성…야외무대·횡단보도교 설치 예고",
      url: "https://www.gukjenews.com/news/articleView.html?idxno=3717346",
    },
  ],

  disclaimer:
    "사이트의 이미지는 연출 이미지로 실제와 다를 수 있습니다. " +
    "사업 내용은 인허가와 설계 확정 과정에서 변경될 수 있습니다.",
};
