/* 공통 레이아웃(헤더·서브비주얼·푸터)과 데이터 블록 렌더링. 데이터는 site-data.js(SSOT). */
(function () {
  "use strict";
  var S = window.SITE;
  var page = document.body.dataset.page || "home";
  var here = location.pathname.split("/").pop() || "index.html";

  function h(tag, attrs, children) {
    var el = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      if (k === "class") el.className = attrs[k];
      else if (k === "text") el.textContent = attrs[k];
      else el.setAttribute(k, attrs[k]);
    });
    (children || []).forEach(function (c) {
      if (c) el.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
    });
    return el;
  }
  function telHref() { return "tel:" + S.contact.tel.replace(/-/g, ""); }
  function isCurrent(item) {
    if (item.href === here) return true;
    return (item.children || []).some(function (c) { return c.href === here; });
  }

  /* 헤더 + 모바일 메뉴 */
  function renderHeader(mount) {
    var list = h("ul", { class: "gnb__list" }, S.nav.map(function (item) {
      var li = h("li", { class: "gnb__item" + (isCurrent(item) ? " is-current" : "") }, [
        h("a", { href: item.href, class: "gnb__link", text: item.label }),
      ]);
      if (item.children) {
        li.appendChild(h("ul", { class: "gnb__sub" }, item.children.map(function (c) {
          return h("li", {}, [h("a", { href: c.href, text: c.label, "aria-current": c.href === here ? "page" : "false" })]);
        })));
      }
      return li;
    }));
    var toggle = h("button", { class: "nav-toggle", type: "button", "aria-expanded": "false", "aria-controls": "gnb", "aria-label": "메뉴 열기" }, [
      h("span"), h("span"), h("span"),
    ]);
    var header = h("header", { class: "site-header" }, [
      h("div", { class: "site-header__inner" }, [
        h("a", { href: "index.html", class: "brand", "aria-label": S.brand.name + " 홈" }, [
          h("img", { src: "assets/img/ai/logo-mark.png", alt: "", width: "40", height: "40" }),
          h("span", { class: "brand__name", text: S.brand.name }),
        ]),
        h("nav", { class: "gnb", id: "gnb", "aria-label": "주 메뉴" }, [list]),
        h("a", { href: telHref(), class: "head-tel" }, [h("span", { class: "head-tel__label", text: "분양 상담" }), S.contact.tel]),
        toggle,
      ]),
    ]);
    toggle.addEventListener("click", function () {
      var open = header.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "메뉴 닫기" : "메뉴 열기");
      document.body.classList.toggle("no-scroll", open);
    });
    mount.replaceWith(header);
  }

  /* 서브 비주얼: 서브 로고 + 영문 타이틀 + 국문 카테고리 */
  function renderSubVisual(mount) {
    var p = S.pages[page];
    if (!p) return;
    var sec = h("section", { class: "sub-visual" }, [
      h("div", { class: "sub-visual__inner" }, [
        h("img", { src: "assets/img/ai/logo-mark.png", alt: "", class: "sub-visual__logo", width: "56", height: "56" }),
        h("h3", { class: "sub-visual__en", text: p.en }),
        h("p", { class: "sub-visual__ko", text: p.ko }),
      ]),
      h("span", { class: "ai-badge", text: "AI 생성 이미지" }),
    ]);
    // url()은 문서 기준 경로로 해석되도록 인라인으로 지정
    sec.style.backgroundImage = "linear-gradient(rgba(30,58,52,.45), rgba(30,58,52,.55)), url('" + p.img + "')";
    mount.replaceWith(sec);
  }

  function renderFooter(mount) {
    mount.replaceWith(h("footer", { class: "site-footer" }, [
      h("div", { class: "site-footer__inner" }, [
        h("p", { class: "site-footer__brand", text: S.brand.name }),
        h("p", {}, ["대표 " + S.brand.owner + " · 전화 ", h("a", { href: telHref(), text: S.contact.tel })]),
        h("p", { class: "site-footer__note", text: S.disclaimer }),
        h("p", { class: "site-footer__copy", text: "© 2026 " + S.brand.name }),
      ]),
    ]));
    document.body.appendChild(h("a", { href: telHref(), class: "call-fab" }, ["전화 상담"]));
  }

  /* 데이터 블록 */
  var blocks = {
    overview: function () {
      return h("table", { class: "spec-table" }, [h("tbody", {}, S.overview.map(function (r) {
        return h("tr", {}, [h("th", { scope: "row", text: r[0] }), h("td", { text: r[1] })]);
      }))]);
    },
    "type-strip": function () {
      return h("ul", { class: "type-strip" }, S.types.map(function (t) {
        return h("li", {}, [h("a", { href: "unit.html#" + t.id }, [
          h("img", { src: t.img, alt: t.name + " 투시도 (AI 생성)", loading: "lazy" }),
          h("span", { class: "type-strip__name", text: t.name }),
          h("span", { class: "type-strip__meta", text: t.title }),
        ])]);
      }));
    },
    types: function () { return renderTypeTabs(); },
    location: function () {
      return h("ul", { class: "loc-list" }, S.location.map(function (l) {
        return h("li", { class: "loc-item loc-item--" + l.kind }, [
          h("h4", { text: l.title }),
          h("p", { text: l.body }),
          l.kind === "fact" && h("p", { class: "loc-item__src" }, [
            "출처: ", h("a", { href: l.src.url, target: "_blank", rel: "noopener", text: l.src.label }),
          ]),
        ]);
      }));
    },
    news: function () {
      return h("ul", { class: "news-list" }, S.news.map(function (n) {
        return h("li", {}, [h("a", { href: n.url, target: "_blank", rel: "noopener" }, [
          h("span", { class: "news-list__press", text: n.press }),
          h("span", { class: "news-list__title", text: n.title }),
          h("time", { datetime: n.date, text: n.date }),
        ])]);
      }));
    },
  };

  function renderTypeTabs() {
    var wrap = h("div", { class: "type-tabs" });
    var tablist = h("div", { class: "type-tabs__list", role: "tablist", "aria-label": "타입별 모듈주택" });
    var panels = [];
    S.types.forEach(function (t, i) {
      var tab = h("button", {
        class: "type-tabs__tab", role: "tab", type: "button", id: "tab-" + t.id,
        "aria-controls": "panel-" + t.id, "aria-selected": "false", tabindex: "-1",
      }, [h("strong", { text: t.name }), h("span", { text: t.title })]);
      tablist.appendChild(tab);
      var panel = h("section", { class: "type-panel", role: "tabpanel", id: "panel-" + t.id, "aria-labelledby": "tab-" + t.id, hidden: "" }, [
        h("figure", { class: "type-panel__fig" }, [
          h("img", { src: t.img, alt: t.name + " " + t.title + " 투시도 (AI 생성)" }),
          h("figcaption", { text: "연출 투시도입니다. 실제 설계와 다를 수 있습니다." }),
        ]),
        h("div", { class: "type-panel__body" }, [
          h("h3", { class: "type-panel__title" }, [t.name + " ", h("span", { text: t.title })]),
          h("p", { class: "type-panel__size", text: S.typeSize }),
          h("table", { class: "spec-table spec-table--compact" }, [h("tbody", {}, t.spec.map(function (r) {
            return h("tr", {}, [h("th", { scope: "row", text: r[0] }), h("td", { text: r[1] })]);
          }))]),
          h("ul", { class: "type-panel__points" }, t.points.map(function (p) { return h("li", { text: p }); })),
          h("p", { class: "type-panel__ref", text: "참고 사례: " + t.ref + " — 타사 시공 사례를 참고한 제안입니다." }),
        ]),
      ]);
      panels.push(panel);
      tab.addEventListener("click", function () { select(i, true); });
    });
    tablist.addEventListener("keydown", function (e) {
      var tabs = tablist.querySelectorAll("[role=tab]");
      var cur = Array.prototype.indexOf.call(tabs, document.activeElement);
      if (cur < 0) return;
      var next = e.key === "ArrowRight" ? cur + 1 : e.key === "ArrowLeft" ? cur - 1 : null;
      if (next === null) return;
      e.preventDefault();
      select((next + tabs.length) % tabs.length, true, true);
    });
    function select(i, updateHash, focus) {
      tablist.querySelectorAll("[role=tab]").forEach(function (tab, k) {
        var on = k === i;
        tab.setAttribute("aria-selected", String(on));
        tab.tabIndex = on ? 0 : -1;
        panels[k].hidden = !on;
        if (on && focus) tab.focus();
      });
      if (updateHash) history.replaceState(null, "", "#" + S.types[i].id);
    }
    wrap.appendChild(tablist);
    panels.forEach(function (p) { wrap.appendChild(p); });
    function fromHash() {
      var k = S.types.findIndex(function (t) { return "#" + t.id === location.hash; });
      select(k < 0 ? 0 : k, false);
    }
    window.addEventListener("hashchange", fromHash);
    fromHash();
    return wrap;
  }

  /* 메인 슬라이드: fade, 8초 자동재생, loop, 이전/다음 버튼 */
  function initSlider(root) {
    var slides = root.querySelectorAll(".hero__slide");
    var counter = root.querySelector(".hero__count");
    var idx = 0, timer = null;
    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    function show(n) {
      slides[idx].classList.remove("is-active");
      slides[idx].setAttribute("aria-hidden", "true");
      idx = (n + slides.length) % slides.length;
      slides[idx].classList.add("is-active");
      slides[idx].setAttribute("aria-hidden", "false");
      if (counter) counter.textContent = (idx + 1) + " / " + slides.length;
    }
    function restart() {
      clearInterval(timer);
      if (!reduce) timer = setInterval(function () { show(idx + 1); }, 8000);
    }
    root.querySelector(".hero__prev").addEventListener("click", function () { show(idx - 1); restart(); });
    root.querySelector(".hero__next").addEventListener("click", function () { show(idx + 1); restart(); });
    show(0);
    restart();
  }

  document.querySelectorAll("[data-mount]").forEach(function (m) {
    var kind = m.dataset.mount;
    if (kind === "header") renderHeader(m);
    else if (kind === "sub-visual") renderSubVisual(m);
    else if (kind === "footer") renderFooter(m);
  });
  document.querySelectorAll("[data-render]").forEach(function (m) {
    var fn = blocks[m.dataset.render];
    if (!fn) throw new Error("unknown data-render: " + m.dataset.render);
    m.appendChild(fn());
  });
  document.querySelectorAll("[data-tel]").forEach(function (a) {
    a.href = telHref();
    a.textContent = S.contact.tel + " " + a.textContent;
  });
  var hero = document.querySelector(".hero");
  if (hero) initSlider(hero);
})();
