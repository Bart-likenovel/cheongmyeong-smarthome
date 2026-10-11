/* 청명스마트홈 사이트 공통 데이터 (SSOT)
 * 연락처·메뉴·사업개요·타입·입지·언론보도는 이 파일만 수정한다.
 * fact: 확인된 사실 / owner: 사업주(대표) 안내 / plan: 계획·검토 단계
 */
window.SITE = {
  brand: { name: "청명스마트홈", en: "Cheongmyeong Smart Home", owner: "유만식" },
  contact: { tel: "010-5001-6182" },

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
    overview: { en: "overview", ko: "사업개요", img: "assets/img/ai/hero-01-village.jpg" },
    premium: { en: "premium", ko: "프리미엄", img: "assets/img/ai/hero-03-interior.jpg" },
    location: { en: "location", ko: "입지환경", img: "assets/img/ai/hero-05-trail.jpg" },
    design: { en: "landscape", ko: "단지안내", img: "assets/img/ai/landscape.jpg" },
    unit: { en: "house types", ko: "단지안내", img: "assets/img/ai/hero-02-yard.jpg" },
    news: { en: "news", ko: "홍보센터", img: "assets/img/ai/hero-06-dusk.jpg" },
  },

  overview: [
    ["사업명", "청명스마트홈"],
    ["위치", "경기도 용인시 기흥구 하갈동 일원 (상세 주소는 상담 시 안내)"],
    ["대지면적", "약 2,000평 (확정 면적 추후 안내)"],
    ["세대수", "13세대 (13필지)"],
    ["주택 유형", "모듈형 스마트 단독주택 (A~E 5개 타입 검토 중)"],
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
      ref: "더존하우징 M25 (사례집 사례 1)",
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
      ref: "경량목구조 33.17평 주택 (사례집 사례 3)",
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
      ref: "더존하우징 DUJON P374 (사례집 사례 2)",
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
      ref: "남양주 목조주택 (사례집 사례 8)",
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
      ref: "적벽돌 주택 (사례집 사례 7)",
    },
  ],

  // 입지 근거. kind: fact(보도·공식 확인) / owner(사업주 안내)
  location: [
    { title: "청명산 기슭", body: "단지가 청명산 기슭에 자리합니다. 숲을 곁에 둔 조용한 주거지입니다.", kind: "owner" },
    { title: "8m 전면 도로 개통 예정", body: "단지 전면에 8m 도로가 2027년 2월 개통될 예정입니다.", kind: "owner" },
    { title: "초등학교 도보권", body: "걸어서 다닐 수 있는 거리에 초등학교가 있습니다.", kind: "owner" },
    {
      title: "하갈동 중학교 신설", kind: "fact",
      body: "하갈동에 기흥중학교(가칭 기흥1중) 신축이 진행되어 2026년 9월 개교 예정으로 보도되었습니다.",
      src: { label: "아시아경제 2026-04-04", url: "https://view.asiae.co.kr/article/2026040417321663186" },
    },
    {
      title: "삼성전자 기흥캠퍼스", kind: "fact",
      body: "삼성전자 기흥캠퍼스(기흥구 농서동)와 같은 기흥구 생활권입니다.",
      src: { label: "삼성전자 반도체 뉴스룸", url: "https://news.samsungsemiconductor.com/kr/%EB%B0%98%EB%8F%84%EC%B2%B4-%EC%97%AD%EC%82%AC%EC%8B%9C%EB%A6%AC%EC%A6%88-6%ED%83%84-%EC%82%BC%EC%84%B1%EB%B0%98%EB%8F%84%EC%B2%B4-45%EB%85%84-%EC%82%AC%EC%97%85%EC%9E%A5%EC%9D%98-%EC%84%B1/" },
    },
    {
      title: "용인 반도체 국가산단", kind: "fact",
      body: "용인시 처인구 이동·남사읍 일대에 삼성전자 반도체 국가산업단지가 조성 중입니다.",
      src: { label: "한국일보 2025-03-14", url: "https://www.hankookilbo.com/News/Read/A2025031408370001371" },
    },
  ],

  news: [
    {
      press: "아시아경제", date: "2026-04-04",
      title: "이상일 용인시장, 기흥중 신축 현장 점검…“통학 안전 조치 즉시 시행”",
      url: "https://view.asiae.co.kr/article/2026040417321663186",
    },
    {
      press: "한국일보", date: "2025-03-14",
      title: "LH, 세계 최대 반도체 생산기지 '용인국가산단' 내년 착공한다",
      url: "https://www.hankookilbo.com/News/Read/A2025031408370001371",
    },
    {
      press: "아주경제", date: "2023-06-23",
      title: "용인시, 기흥구 하갈동에 중학교 신설 최종 결정...\"원거리 통학 어려움 해소될 것\"",
      url: "https://www.ajunews.com/view/20230623092010780",
    },
  ],

  disclaimer:
    "사이트의 이미지는 연출 이미지로 실제와 다를 수 있습니다. " +
    "사업 내용은 인허가와 설계 확정 과정에서 변경될 수 있습니다.",
};
