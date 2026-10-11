/* 사이트 인수 검증: 페이지별 PC/MO 렌더링, 콘솔 오류, 이미지 로드, 가로 넘침, 슬라이드·탭·모바일 메뉴 동작.
 * 사용: NODE_PATH=<playwright 설치 node_modules> node tools/check-site.cjs http://127.0.0.1:8765 <스크린샷 폴더>
 */
const { chromium } = require("playwright");
const BASE = process.argv[2];
const SHOTS = process.argv[3];
const PAGES = ["index", "overview", "premium", "location", "design", "unit", "news"];
const VIEWPORTS = { pc: { width: 1440, height: 900 }, mo: { width: 390, height: 844 } };
const fails = [];
const fail = (m) => { fails.push(m); console.log("FAIL", m); };

(async () => {
  const browser = await chromium.launch();
  for (const [vpName, vp] of Object.entries(VIEWPORTS)) {
    const ctx = await browser.newContext({ viewport: vp, deviceScaleFactor: 1 });
    for (const name of PAGES) {
      const page = await ctx.newPage();
      const errors = [];
      page.on("console", (m) => m.type() === "error" && errors.push(m.text()));
      page.on("pageerror", (e) => errors.push(e.message));
      page.on("requestfailed", (r) => errors.push("requestfailed " + r.url()));
      const res = await page.goto(`${BASE}/${name}.html`, { waitUntil: "networkidle" });
      const tag = `${vpName}/${name}`;
      if (res.status() !== 200) fail(`${tag} status ${res.status()}`);
      // 지연 로드 이미지까지 불러오기
      await page.evaluate(async () => {
        for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo({ top: y, behavior: "instant" }); await new Promise((r) => setTimeout(r, 60)); }
        window.scrollTo({ top: 0, behavior: "instant" });
      });
      await page.waitForLoadState("networkidle");
      const r = await page.evaluate(() => ({
        broken: [...document.images].filter((i) => !i.hidden && i.closest("[hidden]") === null && i.complete && i.naturalWidth === 0).map((i) => i.src),
        overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
        header: !!document.querySelector(".site-header"),
        footerTel: !!document.querySelector(".site-footer a[href^='tel:']"),
        undef: /undefined|null/.test(document.body.innerText),
        unmounted: document.querySelectorAll("[data-mount]").length,
      }));
      if (errors.length) fail(`${tag} console: ${errors.join(" | ")}`);
      if (r.broken.length) fail(`${tag} broken images: ${r.broken.join(", ")}`);
      if (r.overflow > 0) fail(`${tag} horizontal overflow ${r.overflow}px`);
      if (!r.header || !r.footerTel || r.unmounted) fail(`${tag} layout mount missing`);
      if (r.undef) fail(`${tag} 'undefined/null' text rendered`);
      await page.screenshot({ path: `${SHOTS}/${vpName}-${name}.png`, fullPage: true });

      if (name === "index") {
        await page.click(".hero__next");
        const c = await page.textContent(".hero__count");
        if (c.trim() !== "2 / 6") fail(`${tag} slider next -> '${c}'`);
      }
      if (name === "unit") {
        const tabs = await page.$$("[role=tab]");
        if (tabs.length !== 5) fail(`${tag} tab count ${tabs.length}`);
        await page.click("#tab-c");
        const visible = () => [...document.querySelectorAll("[role=tabpanel]")].filter((p) => p.getClientRects().length > 0).map((p) => p.id);
        const vis = await page.evaluate(visible);
        if (vis.join() !== "panel-c") fail(`${tag} tab C -> ${vis}`);
        await page.goto(`${BASE}/unit.html#e`, { waitUntil: "networkidle" });
        const vis2 = await page.evaluate(visible);
        if (vis2.join() !== "panel-e") fail(`${tag} hash #e -> ${vis2}`);
      }
      if (vpName === "mo" && name === "index") {
        await page.click(".nav-toggle");
        const box = await page.evaluate(() => {
          const g = document.querySelector("#gnb").getBoundingClientRect();
          const last = [...document.querySelectorAll(".gnb__link")].pop().getBoundingClientRect();
          return { gh: g.height, lastBottom: last.bottom, vh: innerHeight };
        });
        // 메뉴가 화면 높이의 절반 이상을 차지하고 마지막 메뉴까지 화면 안에 보여야 한다
        if (box.gh < box.vh / 2 || box.lastBottom > box.vh) fail(`${tag} mobile menu clipped ${JSON.stringify(box)}`);
        await page.screenshot({ path: `${SHOTS}/mo-menu.png` });
      }
      await page.close();
    }
    await ctx.close();
  }
  await browser.close();
  console.log(fails.length ? `\n${fails.length} FAIL` : "\nALL PASS");
  process.exit(fails.length ? 1 : 0);
})();
