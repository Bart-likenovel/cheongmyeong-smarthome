// 분양 안내서 PDF 생성. 사이트 루트에서 python3 -m http.server 8765 실행 후:
// NODE_PATH=<playwright node_modules> node tools/make-brochure.cjs <출력 PDF 경로> [기준 URL]
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2], base = process.argv[3] || 'http://127.0.0.1:8765';
  const b = await chromium.launch();
  const p = await b.newPage();
  const errors = [];
  p.on('console', m => m.type() === 'error' && errors.push(m.text()));
  p.on('requestfailed', r => errors.push('failed ' + r.url()));
  await p.goto(base + '/tools/brochure.html');
  await p.waitForFunction('window.BROCHURE_READY === true', null, { timeout: 30000 });
  const over = await p.$$eval('.page', ps => ps.map((el, i) => el.scrollHeight > el.clientHeight + 1 ? i + 1 : 0).filter(Boolean));
  await p.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true });
  await b.close();
  console.log(JSON.stringify({ out, errors, overflowPages: over }));
  if (errors.length || over.length) process.exit(1);
})();
